#!/usr/bin/env python3
import sys
import os

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Current directory:", os.getcwd())

# Test imports
try:
    import json
    print("json: OK")
except ImportError as e:
    print("json: FAILED -", e)

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    print("http.server: OK")
except ImportError as e:
    print("http.server: FAILED -", e)

# Test if we can create a simple server
print("\nTesting simple HTTP server...")
try:
    server = HTTPServer(('127.0.0.1', 7892), BaseHTTPRequestHandler)
    print("Server created successfully on port 7892")
    server.server_close()
    print("Server closed")
except Exception as e:
    print("Server creation failed:", e)

print("\nTest complete")
