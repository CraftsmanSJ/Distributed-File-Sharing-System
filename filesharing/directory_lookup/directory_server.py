import socket
import json
import os
import threading

from common.config import load_peers

# Configuration
UDP_IP = "0.0.0.0"      # Listen on all interfaces
UDP_PORT = 5001         # Port for directory lookup
BUFFER_SIZE = 1024      # Size of UDP packets

# Load shared files
def load_shared_files():
    # Assuming shared_files directory is in file_sharing/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    shared_dir = os.path.join(current_dir, '../file_sharing/shared_files')
    if not os.path.exists(shared_dir):
        os.makedirs(shared_dir)
    files = os.listdir(shared_dir)
    return files

shared_files = load_shared_files()

def handle_search(data, addr, sock):
    """
    Handle incoming search requests.
    Expected data format: {"type": "SEARCH", "filename": "file1.txt"}
    Response format: {"type": "SEARCH_RESPONSE", "filename": "file1.txt", "found": True, "peer_id": "peer1", "ip": "192.168.1.101", "port": 5000}
    """
    try:
        request = json.loads(data.decode())
        if request.get("type") == "SEARCH":
            filename = request.get("filename")
            if filename in shared_files:
                # Assuming this is peer's own info
                peer_info = load_peers()
                if peer_info:
                    peer = peer_info[0]  # Assuming current peer is the first in the list
                    response = {
                        "type": "SEARCH_RESPONSE",
                        "filename": filename,
                        "found": True,
                        "peer_id": peer["id"],
                        "ip": peer["ip"],
                        "port": peer["port"]
                    }
                else:
                    response = {
                        "type": "SEARCH_RESPONSE",
                        "filename": filename,
                        "found": True,
                        "peer_id": "unknown",
                        "ip": "unknown",
                        "port": 0
                    }
            else:
                response = {
                    "type": "SEARCH_RESPONSE",
                    "filename": filename,
                    "found": False
                }
            sock.sendto(json.dumps(response).encode(), addr)
            print("[DIR_LOOKUP] Processed search for '{}' from {}".format(filename, addr))
    except json.JSONDecodeError:
        print("[DIR_LOOKUP] Received invalid JSON from {}".format(addr))
    except Exception as e:
        print("[DIR_LOOKUP] Error processing request from {}: {}".format(addr, e))

def start_directory_lookup_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print("[DIR_LOOKUP] Directory Lookup Server listening on UDP {}:{}".format(UDP_IP, UDP_PORT))

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            threading.Thread(target=handle_search, args=(data, addr, sock)).start()
        except Exception as e:
            print("[DIR_LOOKUP] Server error: {}".format(e))

if __name__ == "__main__":
    start_directory_lookup_server()
