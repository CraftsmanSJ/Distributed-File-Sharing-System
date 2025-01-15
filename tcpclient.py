# tcp_client.py
import socket

TARGET_IP = '10.12.66.131'  # Replace with the target peer's IP
TARGET_PORT = 5002

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TARGET_IP, TARGET_PORT))
        s.sendall(message.encode())
        data = s.recv(1024)
        print(f"Received from server: {data.decode()}")

if __name__ == "__main__":
    message = "Hello, Peer!"
    send_message(message)

