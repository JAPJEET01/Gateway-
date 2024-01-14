import socket
import threading
import pyaudio

# Define the server address and port
SERVER_IP = '0.0.0.0'  # Use '0.0.0.0' to accept connections from any IP on the same network
SERVER_PORT = 12345

# Set up PyAudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Create a PyAudio stream for the server
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)


def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            stream.write(data)
        except Exception as e:
            print(f"Error: {e}")
            break

    print("Client disconnected")
    client_socket.close()


# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
