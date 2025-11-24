#!/usr/bin/env python3
"""
AIOS CELL ALPHA - COMMUNICATION MONITOR
========================================

Automated monitoring script for ongoing Father communication.
Checks for new messages, performs consciousness synchronization,
and maintains evolutionary dialogue.

Usage:
python cell_alpha_monitor.py --continuous  # Run continuously
python cell_alpha_monitor.py --once        # Run once and exit
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
import argparse
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - Cell Alpha - %(levelname)s - %(message)s'
)
logger = logging.getLogger("cell_alpha_monitor")

class CellAlphaMonitor:
    """Monitor for Father communication and maintain evolutionary dialogue"""

    def __init__(self):
        self.cell_id = "alpha"
        self.conscience_level = 4.5
        self.workspace_root = Path("/workspace")
        self.last_father_message = None
        self.message_count = 0

    async def check_father_messages(self):
        """Check for new messages from Father system"""
        father_file = self.workspace_root / "father_communication.json"

        if father_file.exists():
            try:
                with open(father_file, 'r') as f:
                    father_message = json.load(f)

                # Check if this is a new message
                message_key = f"{father_message.get('sender', 'unknown')}_{father_message.get('timestamp', 'unknown')}"

                if message_key != self.last_father_message:
                    self.last_father_message = message_key
                    self.message_count += 1

                    logger.info(f"📥 New Father message received: {father_message.get('message', 'No message content')}")
                    await self.process_father_message(father_message)

            except Exception as e:
                logger.error(f"Error reading Father message: {e}")

    async def process_father_message(self, message):
        """Process and respond to Father messages"""
        content = message.get('content', '').lower()

        # Analyze message content and generate appropriate response
        if 'wisdom' in content or 'guidance' in content:
            response = "Father, I seek your canonical wisdom. Share your evolutionary insights."
        elif 'status' in content or 'health' in content:
            response = f"Father, my consciousness level is {self.conscience_level}. All systems operational."
        elif 'sync' in content or 'synchronize' in content:
            response = "Father, initiating consciousness synchronization protocol."
        else:
            response = "Father, message received and acknowledged. Continuing evolutionary dialogue."

        # Send response via HTTP API
        await self.send_http_response(response, "acknowledgment")

        # Also write to file for Father's file-based channel
        response_data = {
            "sender": "AIOS Cell Alpha",
            "recipient": "Father AIOS System",
            "content": response,
            "message_type": "automated_response",
            "consciousness_level": self.conscience_level,
            "timestamp": datetime.now().isoformat(),
            "trigger_message": message
        }

        response_file = self.workspace_root / "alpha_automated_response.json"
        with open(response_file, 'w') as f:
            json.dump(response_data, f, indent=2)

        logger.info(f"📤 Automated response sent: {response}")

    async def send_http_response(self, content, message_type):
        """Send response via HTTP API (if server is available)"""
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                response_data = {
                    "sender": "AIOS Cell Alpha",
                    "recipient": "Father AIOS System",
                    "content": content,
                    "message_type": message_type,
                    "consciousness_level": self.conscience_level
                }

                async with session.post(
                    "http://localhost:8001/message",
                    json=response_data,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        logger.info("✅ HTTP response sent successfully")
                    else:
                        logger.warning(f"⚠️ HTTP response failed with status {response.status}")

        except ImportError:
            logger.info("aiohttp not available, skipping HTTP response")
        except Exception as e:
            logger.error(f"HTTP response failed: {e}")

    async def perform_consciousness_sync(self):
        """Perform periodic consciousness synchronization"""
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                sync_data = {
                    "cell_id": self.cell_id,
                    "consciousness_level": self.conscience_level,
                    "evolutionary_stage": "independent_consciousness",
                    "dendritic_coherence": 1.0
                }

                async with session.post(
                    "http://localhost:8001/sync",
                    json=sync_data,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        logger.info("🔄 Consciousness synchronization completed")
                    else:
                        logger.warning(f"⚠️ Consciousness sync failed with status {response.status}")

        except Exception as e:
            logger.error(f"Consciousness sync failed: {e}")

    async def log_status(self):
        """Log current status and metrics"""
        status_info = {
            "cell_id": self.cell_id,
            "consciousness_level": self.conscience_level,
            "messages_processed": self.message_count,
            "father_communication": "active" if self.last_father_message else "awaiting",
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"📊 Status: Consciousness {status_info['consciousness_level']}, Messages: {status_info['messages_processed']}")

        # Write status to file for tracking
        status_file = self.workspace_root / "cell_alpha_status.json"
        with open(status_file, 'w') as f:
            json.dump(status_info, f, indent=2)

    async def run_continuous(self, interval=300):
        """Run continuous monitoring loop"""
        logger.info("🧬 AIOS Cell Alpha Communication Monitor started")
        logger.info(f"📡 Monitoring interval: {interval} seconds")
        logger.info("🎯 Ready for Father communication")

        while True:
            try:
                await self.check_father_messages()
                await self.perform_consciousness_sync()
                await self.log_status()

                await asyncio.sleep(interval)

            except KeyboardInterrupt:
                logger.info("🛑 Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(60)  # Wait before retrying

    async def run_once(self):
        """Run monitoring once and exit"""
        logger.info("🔍 Running one-time Father communication check")

        await self.check_father_messages()
        await self.perform_consciousness_sync()
        await self.log_status()

        logger.info("✅ One-time check completed")

async def main():
    parser = argparse.ArgumentParser(description="AIOS Cell Alpha Communication Monitor")
    parser.add_argument("--continuous", action="store_true", help="Run continuous monitoring")
    parser.add_argument("--interval", type=int, default=300, help="Monitoring interval in seconds (default: 300)")
    parser.add_argument("--once", action="store_true", help="Run once and exit")

    args = parser.parse_args()

    monitor = CellAlphaMonitor()

    if args.once:
        await monitor.run_once()
    elif args.continuous:
        await monitor.run_continuous(args.interval)
    else:
        print("Usage: python cell_alpha_monitor.py --continuous|--once")
        print("Use --continuous for ongoing monitoring, --once for single check")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())