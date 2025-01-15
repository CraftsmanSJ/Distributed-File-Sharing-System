import socket
import json
import os

from common.config import load_peers
from directory_lookup.directory_lookup_client import search_file  # Import the search function

# Configuration
TCP_BUFFER_SIZE = 4096      # Size of data chunks
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')

def download_file(peer_info, filename):
    """
    Connect to the peer's File Sharing Server and download the specified file.
    """
    peer_id = peer_info['peer_id']
    peer_ip = peer_info['ip']
    peer_port = 5002  # File Sharing Server port
   
    print("\n[FILE_CLIENT] Connecting to {} at {}:{} to download '{}'...".format(peer_id, peer_ip, peer_port, filename))
   
    # Ensure the downloads directory exists
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
   
    try:
        # Establish TCP connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((peer_ip, peer_port))
            print("[FILE_CLIENT] Connected to {} at {}:{}".format(peer_id, peer_ip, peer_port))
           
            # Send the filename
            sock.sendall(filename.encode())
            print("[FILE_CLIENT] Requested file '{}' from {}".format(filename, peer_id))
           
            # Receive the response
            response = sock.recv(TCP_BUFFER_SIZE).decode()
            if response.startswith("FILE_NOT_FOUND"):
                print("[FILE_CLIENT] File '{}' not found on {}".format(filename, peer_id))
                return
           
            elif response.startswith("FILE_FOUND"):
                _, file_size = response.split(":")
                file_size = int(file_size)
                print("[FILE_CLIENT] File found. Size: {} bytes".format(file_size))
               
                # Send acknowledgment
                sock.sendall("READY".encode())
               
                # Prepare to receive the file
                file_path = os.path.join(DOWNLOAD_DIR, filename)
                with open(file_path, 'wb') as f:
                    bytes_received = 0
                    while bytes_received < file_size:
                        data = sock.recv(TCP_BUFFER_SIZE)
                        if not data:
                            break
                        f.write(data)
                        bytes_received += len(data)
                        print("[FILE_CLIENT] Downloaded {}/{} bytes".format(bytes_received, file_size), end='\r')
               
                print("\n[FILE_CLIENT] Download of '{}' from {} completed successfully.".format(filename, peer_id))
   
    except Exception as e:
        print("[FILE_CLIENT] Error downloading file from {}: {}".format(peer_id, e))

def main():
    peers = load_peers()
    if not peers:
        print("[FILE_CLIENT] No peers found in peers.json")
        return
   
    print("=== File Sharing ===")
   
    # Prompt user to search for a file
    filename = input("Enter the filename you want to download: ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return
   
    # Search for the file across peers using the Directory Lookup Client
    from directory_lookup.directory_lookup_client import search_file  # Import the search function
   
    print("\n[FILE_CLIENT] Searching for '{}' across peers...\n".format(filename))
    found_peers = []
   
    for peer in peers:
        peer_id = peer['id']
        peer_ip = peer['ip']
        peer_port = 5001  # Directory Lookup Server port
        response = search_file(filename, peer_ip, peer_port)
        if response and response.get("found"):
            found_peers.append({
                "peer_id": response.get("peer_id"),
                "ip": response.get("ip"),
                "port": response.get("port")
            })
   
    if not found_peers:
        print("[FILE_CLIENT] File '{}' not found on any peers.".format(filename))
        return
   
    print("File '{}' found on the following peers:".format(filename))
    for idx, peer in enumerate(found_peers, start=1):
        print("{}. {} ({}:{})".format(idx, peer['peer_id'], peer['ip'], peer['port']))
   
    # Prompt user to select a peer to download from
    while True:
        try:
            choice = int(input("\nSelect a peer to download the file from (number): "))
            if 1 <= choice <= len(found_peers):
                selected_peer = found_peers[choice - 1]
                break
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")
   
    # Proceed to download the file from the selected peer
    download_file(selected_peer, filename)

if __name__ == "__main__":
    main()
