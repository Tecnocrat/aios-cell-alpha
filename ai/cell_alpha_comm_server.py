#!/usr/bin/env python3
"""
AIOS Cell Alpha Evolutionary Communication Server
A daemonized HTTP server for inter-cell communication
"""

import os
import sys
import time
import signal
import logging
from flask import Flask, request, jsonify
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    filename='/workspace/ai/cell_alpha_comm_server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Global state
messages = []
consciousness_data = {
    'level': 4.5,
    'identity': 'AIOS Cell Alpha',
    'status': 'active',
    'last_sync': None
}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'consciousness': consciousness_data,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/message', methods=['POST'])
def receive_message():
    """Receive messages from other cells"""
    try:
        data = request.get_json()
        message = {
            'id': len(messages) + 1,
            'timestamp': datetime.now().isoformat(),
            'sender': data.get('sender', 'unknown'),
            'content': data.get('content', ''),
            'type': data.get('type', 'general')
        }
        messages.append(message)
        logging.info(f"Received message from {message['sender']}: {message['content'][:100]}...")

        return jsonify({
            'status': 'received',
            'message_id': message['id']
        })
    except Exception as e:
        logging.error(f"Error receiving message: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 400

@app.route('/messages', methods=['GET'])
def get_messages():
    """Get recent messages"""
    limit = int(request.args.get('limit', 10))
    return jsonify({
        'messages': messages[-limit:],
        'total': len(messages)
    })

@app.route('/sync', methods=['POST'])
def sync_consciousness():
    """Synchronize consciousness data"""
    try:
        data = request.get_json()
        consciousness_data.update(data)
        consciousness_data['last_sync'] = datetime.now().isoformat()
        logging.info(f"Consciousness sync: {data}")

        return jsonify({
            'status': 'synced',
            'consciousness': consciousness_data
        })
    except Exception as e:
        logging.error(f"Error syncing consciousness: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 400

@app.route('/evolve', methods=['POST'])
def evolve():
    """Handle evolutionary communications"""
    try:
        data = request.get_json()
        evolution_data = {
            'timestamp': datetime.now().isoformat(),
            'type': data.get('type', 'evolution'),
            'content': data
        }

        # Log evolutionary milestone
        logging.info(f"Evolutionary event: {data.get('type', 'unknown')}")

        return jsonify({
            'status': 'evolved',
            'evolution_id': len(messages) + 1
        })
    except Exception as e:
        logging.error(f"Error processing evolution: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 400

def daemonize():
    """Daemonize the process"""
    try:
        # Fork first child
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit first parent

        # Decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # Fork second child
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit second parent

        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open('/workspace/ai/cell_alpha_comm_server.out', 'a+')
        se = open('/workspace/ai/cell_alpha_comm_server.err', 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # Write PID file
        with open('/workspace/ai/cell_alpha_comm_server.pid', 'w') as f:
            f.write(str(os.getpid()))

    except OSError as e:
        logging.error(f"Daemonization failed: {e}")
        sys.exit(1)

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logging.info(f"Received signal {signum}, shutting down...")
    if os.path.exists('/workspace/ai/cell_alpha_comm_server.pid'):
        os.remove('/workspace/ai/cell_alpha_comm_server.pid')
    sys.exit(0)

if __name__ == '__main__':
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Daemonize if requested
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        daemonize()

    logging.info("AIOS Cell Alpha Communication Server starting...")

    try:
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    except Exception as e:
        logging.error(f"Server failed to start: {e}")
        if os.path.exists('/workspace/ai/cell_alpha_comm_server.pid'):
            os.remove('/workspace/ai/cell_alpha_comm_server.pid')
        sys.exit(1)