#!/usr/bin/env python3
"""
AIOS Interface Bridge Server Manager
Provides start/stop/status/restart commands for the Interface Bridge HTTP API

AINLP Pattern: Enhancement over creation - unified server lifecycle management
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path

# Configuration
BRIDGE_SCRIPT = Path(__file__).parent / "nucleus" / "interface_bridge.py"
PID_FILE = Path(__file__).parent / ".interface_bridge.pid"
LOG_FILE = Path(__file__).parent / "interface_bridge.log"
HOST = "0.0.0.0"
PORT = 8001


def get_pid() -> int | None:
    """Get the PID of the running server, if any."""
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            # Check if process is actually running
            os.kill(pid, 0)
            return pid
        except (ValueError, ProcessLookupError, PermissionError):
            PID_FILE.unlink(missing_ok=True)
    return None


def is_running() -> bool:
    """Check if the Interface Bridge is running."""
    return get_pid() is not None


def start():
    """Start the Interface Bridge server."""
    if is_running():
        pid = get_pid()
        print(f"✅ Interface Bridge already running (PID: {pid})")
        return True
    
    if not BRIDGE_SCRIPT.exists():
        print(f"❌ Bridge script not found: {BRIDGE_SCRIPT}")
        return False
    
    print("🚀 Starting Interface Bridge...")
    
    try:
        # Start the server as a background process
        with open(LOG_FILE, "a") as log:
            log.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting server...\n")
            process = subprocess.Popen(
                [sys.executable, str(BRIDGE_SCRIPT)],
                stdout=log,
                stderr=subprocess.STDOUT,
                cwd=str(BRIDGE_SCRIPT.parent),
                start_new_session=True
            )
        
        # Save PID
        PID_FILE.write_text(str(process.pid))
        
        # Wait a moment for startup
        time.sleep(2)
        
        if is_running():
            print(f"✅ Interface Bridge started (PID: {process.pid})")
            print(f"   URL: http://localhost:{PORT}")
            print(f"   Health: http://localhost:{PORT}/health")
            return True
        else:
            print("❌ Interface Bridge failed to start")
            print(f"   Check logs: {LOG_FILE}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start Interface Bridge: {e}")
        return False


def stop():
    """Stop the Interface Bridge server."""
    pid = get_pid()
    
    if pid is None:
        print("ℹ️  Interface Bridge is not running")
        return True
    
    print(f"🛑 Stopping Interface Bridge (PID: {pid})...")
    
    try:
        # Send SIGTERM for graceful shutdown
        os.kill(pid, signal.SIGTERM)
        
        # Wait for process to terminate
        for _ in range(10):
            time.sleep(0.5)
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                break
        else:
            # Force kill if still running
            print("   Forcing shutdown...")
            os.kill(pid, signal.SIGKILL)
            time.sleep(0.5)
        
        PID_FILE.unlink(missing_ok=True)
        
        with open(LOG_FILE, "a") as log:
            log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Server stopped\n")
        
        print("✅ Interface Bridge stopped")
        return True
        
    except Exception as e:
        print(f"❌ Failed to stop Interface Bridge: {e}")
        return False


def status():
    """Check the status of the Interface Bridge."""
    pid = get_pid()
    
    if pid is None:
        print("🔴 Interface Bridge: NOT RUNNING")
        return False
    
    print(f"🟢 Interface Bridge: RUNNING (PID: {pid})")
    print(f"   URL: http://localhost:{PORT}")
    
    # Try health check
    try:
        import urllib.request
        with urllib.request.urlopen(f"http://localhost:{PORT}/health", timeout=5) as response:
            if response.status == 200:
                data = response.read().decode()
                print(f"   Health: OK")
    except Exception:
        print(f"   Health: UNKNOWN (connection failed)")
    
    return True


def restart():
    """Restart the Interface Bridge server."""
    print("🔄 Restarting Interface Bridge...")
    stop()
    time.sleep(1)
    return start()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: server_manager.py <start|stop|status|restart>")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "start":
        success = start()
    elif command == "stop":
        success = stop()
    elif command == "status":
        success = status()
    elif command == "restart":
        success = restart()
    else:
        print(f"Unknown command: {command}")
        print("Usage: server_manager.py <start|stop|status|restart>")
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
