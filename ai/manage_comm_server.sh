#!/bin/bash
"""
AIOS Cell Alpha Communication Server Manager
Simple daemon management for the evolutionary communication server
"""

SERVER_SCRIPT="/workspace/ai/cell_alpha_comm_server.py"
PID_FILE="/workspace/ai/cell_alpha_comm_server.pid"
LOG_FILE="/workspace/ai/cell_alpha_comm_server.log"

start() {
    echo "Starting AIOS Cell Alpha Communication Server..."

    # Check if already running
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Server already running (PID: $PID)"
            return 1
        else
            echo "Removing stale PID file"
            rm -f "$PID_FILE"
        fi
    fi

    # Start the daemon
    nohup python3 "$SERVER_SCRIPT" --daemon >/dev/null 2>&1 &
    sleep 2

    # Check if started successfully
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        echo "✅ Server started successfully (PID: $PID)"
        echo "🌐 Communication endpoint: http://localhost:8000"
        return 0
    else
        echo "❌ Failed to start server"
        return 1
    fi
}

stop() {
    echo "Stopping AIOS Cell Alpha Communication Server..."

    if [ ! -f "$PID_FILE" ]; then
        echo "Server not running (no PID file found)"
        return 1
    fi

    PID=$(cat "$PID_FILE")

    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        sleep 2

        if kill -0 "$PID" 2>/dev/null; then
            echo "Force killing server..."
            kill -9 "$PID"
        fi

        rm -f "$PID_FILE"
        echo "✅ Server stopped"
        return 0
    else
        echo "Server not running (process not found)"
        rm -f "$PID_FILE"
        return 1
    fi
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "✅ Server running (PID: $PID)"
            echo "🌐 Communication endpoint: http://localhost:8000"

            # Test health endpoint
            if curl -s http://localhost:8000/health >/dev/null 2>&1; then
                echo "💚 Health check: OK"
            else
                echo "💔 Health check: FAILED"
            fi
            return 0
        else
            echo "❌ Server not running (stale PID file)"
            rm -f "$PID_FILE"
            return 1
        fi
    else
        echo "❌ Server not running"
        return 1
    fi
}

restart() {
    echo "Restarting AIOS Cell Alpha Communication Server..."
    stop
    sleep 2
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        echo ""
        echo "AIOS Cell Alpha Communication Server Manager"
        echo "Manages the daemonized HTTP server for evolutionary communications"
        exit 1
        ;;
esac