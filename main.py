#!/usr/bin/env python3
"""
Quantum Maze Web Server for Wasmer
Serves the HTML5 game on Wasmer Edge
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

class QuantumMazeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for web compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def do_GET(self):
        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Custom logging for Wasmer
        print(f"🌌 Quantum Maze: {format % args}")

def main():
    # Get port from environment or default to 8000
    PORT = int(os.environ.get('PORT', 8000))
    HOST = os.environ.get('HOST', '0.0.0.0')  # Bind to all interfaces for Wasmer
    
    print("🌌" + "="*60 + "🌌")
    print("    QUANTUM MAZE - Web Server Starting")
    print("    AWS Build Games Challenge Entry")
    print("    Built with Amazon Q Developer CLI")
    print("🌌" + "="*60 + "🌌")
    print()
    print(f"🚀 Starting Quantum Maze Web Server...")
    print(f"🌐 Host: {HOST}")
    print(f"🔌 Port: {PORT}")
    print(f"📁 Serving from: {os.getcwd()}")
    print()
    
    # Check if index.html exists
    if not os.path.exists('index.html'):
        print("❌ Error: index.html not found!")
        print("📁 Current directory contents:")
        for item in os.listdir('.'):
            print(f"   - {item}")
        sys.exit(1)
    
    try:
        with socketserver.TCPServer((HOST, PORT), QuantumMazeHandler) as httpd:
            print(f"✅ Quantum Maze server running at http://{HOST}:{PORT}")
            print("🎮 Game ready! Open the URL in your browser to play.")
            print("🏆 #BuildGamesChallenge #AmazonQDevCLI")
            print()
            print("Press Ctrl+C to stop the server")
            print("-" * 60)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
