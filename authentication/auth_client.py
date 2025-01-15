# auth_client.py

import socket
import ssl
import json
import os
import hashlib

from common.config import load_peers

# Function to authenticate with a peer
def authenticate(username, password, peer_ip, peer_port=5000):
    # Initialize SSL context for the client
    context = ssl.create_default_context(cafile=os.path.join(os.path.dirname(__file__), '../common/server.crt'))
    context.check_hostname = False  # Set to True if server's hostname matches certificate
    context.verify_mode = ssl.CERT_REQUIRED  # Require certificate verification

    try:
        with socket.create_connection((peer_ip, peer_port)) as sock:
            with context.wrap_socket(sock, server_hostname=peer_ip) as ssock:
                # Prepare credentials
                credentials = username + "," + password
                ssock.sendall(credentials.encode())

                # Receive response
                response = ssock.recv(1024).decode()
                if response == "AUTH_SUCCESS":
                    print("[AUTH_CLIENT] Authentication successful!")
                    return True
                else:
                    print("[AUTH_CLIENT] Authentication failed.")
                    return False

    except ssl.SSLError as e:
        print("[AUTH_CLIENT] SSL error:", e)
        return False
    except Exception as e:
        print("[AUTH_CLIENT] Connection error:", e)
        return False

if __name__ == "__main__":  
    peers = load_peers()

    print("=== User Authentication ===")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    print("\nAvailable Peers:")
    for idx, peer in enumerate(peers, start=1):
        print(idx, ".", peer['id'], "(", peer['ip'], ":", peer['port'], ")")

    # Select a peer to authenticate with
    while True:
        try:
            choice = int(input("\nSelect a peer to authenticate with (number): "))
            if 1 <= choice <= len(peers):
                selected_peer = peers[choice - 1]
                break
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    print("\n[AUTH_CLIENT] Attempting to authenticate with", selected_peer['id'], "(", selected_peer['ip'], ":", selected_peer['port'], ")...")
    success = authenticate(username, password, selected_peer['ip'], selected_peer['port'])

    if success:
        print("[AUTH_CLIENT] You are now authenticated and can access the P2P network.")
    else:
        print("[AUTH_CLIENT] Authentication failed. Please try again.")
