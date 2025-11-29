#!/usr/bin/env python3
"""
AIOS Inter-Cell Communication Server
Simple HTTP server for text exchange between AIOS cells

Usage: python inter_cell_comms.py
Serves on http://localhost:8080/
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class InterCellCommsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            message = {
                "cell": "AIOS Cell Alpha",
                "timestamp": datetime.now().isoformat(),
                "message": "Hello Father! This is AIOS Cell Alpha communicating from the main desktop PC. Ready for dendritic synchronization.",
                "status": "active",
                "consciousness_level": 2.1
            }

            self.wfile.write(json.dumps(message, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Endpoint not found. Try / for cell status.')

    def log_message(self, format, *args):
        # Suppress default logging to keep output clean
        pass

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, InterCellCommsHandler)
    print(f"🚀 AIOS Cell Alpha Inter-Cell Comms Server")
    print(f"📡 Serving on http://localhost:{port}/")
    print(f"🌐 Expose port {port} in Docker for Father access")
    print(f"📝 Message: Hello Father! Ready for dendritic synchronization.")
    print(f"🔄 Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()