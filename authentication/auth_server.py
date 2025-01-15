# auth_server.py

import socket
import ssl
import json
import os
import threading
import hashlib

from common.config import load_peers  # Ensure this function exists or comment it out if not needed

# Load user data
def load_users():
    config_path = os.path.join(os.path.dirname(__file__), 'users.json')
    with open(config_path, 'r') as f:
        data = json.load(f)
    return data['users']

users = load_users()

# Function to handle client connections
def handle_client(conn, addr):
    print("[AUTH] Connected by", addr)
    try:
        # Receive credentials
        data = conn.recv(1024).decode()
        if not data:
            print("[AUTH] No data received from", addr)
            return
        username, password = data.strip().split(',')
        print("[AUTH] Received credentials from", username)

        # Hash the received password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Validate credentials
        if username in users and users[username] == hashed_password:
            response = "AUTH_SUCCESS"
            print("[AUTH] User", username, "authenticated successfully.")
        else:
            response = "AUTH_FAIL"
            print("[AUTH] Authentication failed for user", username)

        # Send response
        conn.sendall(response.encode())

    except Exception as e:
        print("[AUTH] Error handling client", addr, ":", e)
    finally:
        conn.close()
        print("[AUTH] Connection with", addr, "closed.")

# Function to start the authentication server
def start_auth_server(host='0.0.0.0', port=5000):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # Load server's certificate and private key
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bindsocket.bind((host, port))
    bindsocket.listen(5)
    print("[AUTH] Authentication server listening on", host, ":", port)

    with context.wrap_socket(bindsocket, server_side=True) as ssock:
        while True:
            try:
                conn, addr = ssock.accept()
                # Handle client in a new thread
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
            except Exception as e:
                print("[AUTH] Server error:", e)

if __name__ == "__main__":
    start_auth_server()
