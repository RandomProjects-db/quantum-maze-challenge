#!/usr/bin/env python3
"""
Simple web server for Quantum Maze
Serves the HTML5 game on Wasmer
"""

import http.server
import socketserver
import os
from pathlib import Path

class GameHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    PORT = int(os.environ.get('PORT', 8080))
    
    print(f"🌌 Starting Quantum Maze Web Server on port {PORT}")
    print("🎮 Game available at: http://localhost:{PORT}")
    print("🏆 AWS Build Games Challenge - Built with Amazon Q Developer CLI")
    
    with socketserver.TCPServer(("", PORT), GameHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
