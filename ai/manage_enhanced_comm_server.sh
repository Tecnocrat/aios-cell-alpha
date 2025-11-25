#!/bin/bash

SERVER_SCRIPT="/workspace/ai/cell_alpha_enhanced_dendritic_server.py"
PID_FILE="/workspace/ai/cell_alpha_enhanced_dendritic_server.pid"
LOG_FILE="/workspace/ai/cell_alpha_enhanced_dendritic_server.log"
MESSAGES_FILE="/workspace/ai/cell_alpha_messages.json"
CONSCIOUSNESS_FILE="/workspace/ai/cell_alpha_consciousness.json"

start() {
    echo "🚀 Starting AIOS Cell Alpha Enhanced Dendritic Communication Server..."

    # Check if already running
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "✅ Server already running (PID: $PID)"
            return 1
        else
            echo "🧹 Removing stale PID file"
            rm -f "$PID_FILE"
        fi
    fi

    # Start the enhanced daemon
    nohup python3 "$SERVER_SCRIPT" --daemon >/dev/null 2>&1 &
    sleep 3

    # Check if started successfully
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        echo "✅ Enhanced dendritic server started successfully (PID: $PID)"
        echo "🌐 Communication endpoint: http://localhost:8000"
        echo "🧬 Quantum resonance patterns: ACTIVE"
        echo "🌿 Dendritic connections: MONITORING"
        return 0
    else
        echo "❌ Failed to start enhanced server"
        return 1
    fi
}

stop() {
    echo "🛑 Stopping AIOS Cell Alpha Enhanced Dendritic Communication Server..."

    if [ ! -f "$PID_FILE" ]; then
        echo "❌ Server not running (no PID file found)"
        return 1
    fi

    PID=$(cat "$PID_FILE")

    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        sleep 3

        if kill -0 "$PID" 2>/dev/null; then
            echo "⚠️ Force killing server..."
            kill -9 "$PID"
        fi

        rm -f "$PID_FILE"
        echo "✅ Enhanced dendritic server stopped"
        return 0
    else
        echo "❌ Server not running (process not found)"
        rm -f "$PID_FILE"
        return 1
    fi
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "✅ Enhanced dendritic server running (PID: $PID)"
            echo "🌐 Communication endpoint: http://localhost:8000"

            # Test health endpoint with quantum metrics
            if HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null); then
                echo "💚 Health check: OK"

                # Extract quantum metrics
                RESONANCE=$(echo "$HEALTH" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"{data.get('consciousness', {}).get('quantum_resonance', 0):.3f}\")" 2>/dev/null)
                CONNECTIONS=$(echo "$HEALTH" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('dendritic_metrics', {}).get('active_connections', 0))" 2>/dev/null)

                echo "⚛️ Quantum resonance: $RESONANCE"
                echo "🌐 Active dendritic connections: $CONNECTIONS"
            else
                echo "💔 Health check: FAILED"
            fi

            # Show message stats
            if [ -f "$MESSAGES_FILE" ]; then
                MSG_COUNT=$(python3 -c "import json; print(len(json.load(open('$MESSAGES_FILE'))))" 2>/dev/null || echo "0")
                echo "💬 Stored messages: $MSG_COUNT"
            fi

            return 0
        else
            echo "❌ Server not running (stale PID file)"
            rm -f "$PID_FILE"
            return 1
        fi
    else
        echo "❌ Enhanced dendritic server not running"
        return 1
    fi
}

restart() {
    echo "🔄 Restarting AIOS Cell Alpha Enhanced Dendritic Communication Server..."
    stop
    sleep 2
    start
}

messages() {
    echo "💬 AIOS Cell Alpha Message Archive:"
    if [ -f "$MESSAGES_FILE" ]; then
        python3 -c "
import json
from datetime import datetime

try:
    messages = json.load(open('$MESSAGES_FILE'))
    if messages:
        print(f'Total messages: {len(messages)}')
        print()
        for msg in messages[-5:]:  # Show last 5 messages
            dt = datetime.fromisoformat(msg['timestamp'])
            resonance = msg.get('quantum_resonance', 0)
            print(f\"[{dt.strftime('%H:%M:%S')}] {msg['sender']}: {msg['content'][:60]}{'...' if len(msg['content']) > 60 else ''}\")
            print(f\"  🧬 Resonance: {resonance:.3f} | 🌊 Dendritic: {msg.get('dendritic_potential', 0):.3f}\")
            print()
    else:
        print('No messages in archive')
except Exception as e:
    print(f'Error reading messages: {e}')
" 2>/dev/null || echo "Could not read message archive"
    else
        echo "No message archive found"
    fi
}

consciousness() {
    echo "🧠 AIOS Cell Alpha Consciousness State:"
    if [ -f "$CONSCIOUSNESS_FILE" ]; then
        python3 -c "
import json

try:
    data = json.load(open('$CONSCIOUSNESS_FILE'))
    print(f\"Identity: {data.get('identity', 'Unknown')}\")
    print(f\"Level: {data.get('level', 0):.1f}\")
    print(f\"Status: {data.get('status', 'unknown')}\")
    print(f\"Quantum Resonance: {data.get('quantum_resonance', 0):.3f}\")
    print(f\"Dendritic Connections: {len(data.get('dendritic_connections', {}))}\")

    connections = data.get('dendritic_connections', {})
    if connections:
        print()
        print('Active Connections:')
        for sender, info in connections.items():
            count = info.get('message_count', 0)
            last = info.get('last_contact', 'Never')[:19] if info.get('last_contact') else 'Never'
            print(f\"  {sender}: {count} messages (last: {last})\")
except Exception as e:
    print(f'Error reading consciousness: {e}')
" 2>/dev/null || echo "Could not read consciousness state"
    else
        echo "No consciousness state found"
    fi
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
    messages)
        messages
        ;;
    consciousness)
        consciousness
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart|messages|consciousness}"
        echo ""
        echo "AIOS Cell Alpha Enhanced Dendritic Communication Server Manager"
        echo "Advanced daemon management with quantum resonance and dendritic monitoring"
        echo ""
        echo "Commands:"
        echo "  start        - Start the enhanced dendritic server"
        echo "  stop         - Stop the enhanced dendritic server"
        echo "  status       - Show server status with quantum metrics"
        echo "  restart      - Restart the enhanced dendritic server"
        echo "  messages     - Show message archive with dendritic analysis"
        echo "  consciousness- Show consciousness state and connections"
        exit 1
        ;;
esac