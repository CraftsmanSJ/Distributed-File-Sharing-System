import socket
import json
import os
import time

from common.config import load_peers

# Configuration
UDP_PORT = 5001         # Port for directory lookup
BUFFER_SIZE = 1024      # Size of UDP packets
TIMEOUT = 2             # Timeout in seconds for responses

def search_file(filename, peer_ip, peer_port=5001):
    """
    Send a search request to a specific peer.
    Returns the response if any, else None.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    request = {
        "type": "SEARCH",
        "filename": filename
    }
    try:
        sock.sendto(json.dumps(request).encode(), (peer_ip, peer_port))
        data, _ = sock.recvfrom(BUFFER_SIZE)
        response = json.loads(data.decode())
        return response
    except socket.timeout:
        print("[DIR_LOOKUP_CLIENT] No response from {}:{}".format(peer_ip, peer_port))
    except json.JSONDecodeError:
        print("[DIR_LOOKUP_CLIENT] Received invalid JSON from {}:{}".format(peer_ip, peer_port))
    except Exception as e:
        print("[DIR_LOOKUP_CLIENT] Error communicating with {}:{}: {}".format(peer_ip, peer_port, e))
    finally:
        sock.close()
    return None

def main():
    peers = load_peers()
    if not peers:
        print("[DIR_LOOKUP_CLIENT] No peers found in peers.json")
        return

    print("=== Directory Lookup ===")
    filename = input("Enter the filename to search for: ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return

    print("\n[DIR_LOOKUP_CLIENT] Searching for '{}' across peers...\n".format(filename))
    found_peers = []

    for peer in peers:
        peer_id = peer['id']
        peer_ip = peer['ip']
        peer_port = UDP_PORT  # Directory Lookup Server runs on UDP_PORT
        response = search_file(filename, peer_ip, peer_port)
        if response and response.get("found"):
            found_peers.append({
                "peer_id": response.get("peer_id"),
                "ip": response.get("ip"),
                "port": response.get("port")
            })

    if found_peers:
        print("File '{}' found on the following peers:".format(filename))
        for peer in found_peers:
            print("- {} ({}:{})".format(peer['peer_id'], peer['ip'], peer['port']))
    else:
        print("File '{}' not found on any peers.".format(filename))

if __name__ == "__main__":
    main()
