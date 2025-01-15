import socket
import threading
import os

from common.config import load_peers

# Configuration
TCP_IP = "0.0.0.0"          # Listen on all interfaces
TCP_PORT = 5002             # Port for file sharing
BUFFER_SIZE = 4096          # Size of data chunks

# Path to shared files directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SHARED_DIR = os.path.join(CURRENT_DIR, 'shared_files')

def handle_client(conn, addr):
    print("[FILE_SERVER] Connection established with {}".format(addr))
    try:
        # Receive the filename from the client
        filename = conn.recv(BUFFER_SIZE).decode().strip()
        print("[FILE_SERVER] Client {} requested file: '{}'".format(addr, filename))
       
        # Construct the full file path
        file_path = os.path.join(SHARED_DIR, filename)
       
        # Check if the file exists
        if not os.path.isfile(file_path):
            response = "FILE_NOT_FOUND"
            conn.sendall(response.encode())
            print("[FILE_SERVER] File '{}' not found. Sent 'FILE_NOT_FOUND' to {}".format(filename, addr))
            return
       
        # Send file size first
        file_size = os.path.getsize(file_path)
        response = "FILE_FOUND:{}".format(file_size)
        conn.sendall(response.encode())
        print("[FILE_SERVER] File '{}' found. Sent 'FILE_FOUND:{}' to {}".format(filename, file_size, addr))
       
        # Wait for client's acknowledgment
        ack = conn.recv(BUFFER_SIZE).decode()
        if ack != "READY":
            print("[FILE_SERVER] Client {} not ready to receive the file.".format(addr))
            return
       
        # Start sending the file in chunks
        with open(file_path, 'rb') as f:
            bytes_sent = 0
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                conn.sendall(data)
                bytes_sent += len(data)
                print("[FILE_SERVER] Sent {}/{} bytes to {}".format(bytes_sent, file_size, addr))
       
        print("[FILE_SERVER] Completed sending '{}' to {}".format(filename, addr))
   
    except Exception as e:
        print("[FILE_SERVER] Error with client {}: {}".format(addr, e))
   
    finally:
        conn.close()
        print("[FILE_SERVER] Connection with {} closed.".format(addr))

def start_file_server(host='0.0.0.0',port=5002):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(5)
    print("[FILE_SERVER] File Sharing Server listening on {}:{}".format(TCP_IP, TCP_PORT))
   
    while True:
        try:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
        except Exception as e:
            print("[FILE_SERVER] Server error: {}".format(e))

if __name__ == "__main__":
    start_file_server()
