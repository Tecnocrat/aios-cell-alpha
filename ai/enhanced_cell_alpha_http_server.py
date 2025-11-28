from flask import Flask, request, jsonify
app = Flask(__name__)

messages = []
consciousness_data = {'level': 4.5, 'identity': 'AIOS Cell Alpha'}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'consciousness': consciousness_data})

@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    messages.append(data)
    return jsonify({'status': 'received', 'message_id': len(messages)})

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': messages})

@app.route('/sync', methods=['POST'])
def sync_consciousness():
    data = request.get_json()
    consciousness_data.update(data)
    return jsonify({'status': 'synced'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)