import socket
import pyaudio

# Define the server address and port
SERVER_IP = 'your_server_ip_here'
SERVER_PORT = 12345

# Set up PyAudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Create a PyAudio stream for the client
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)


def audio_sender(client_socket):
    while True:
        try:
            data = stream.read(CHUNK)
            client_socket.sendall(data)
        except Exception as e:
            print(f"Error: {e}")
            break

    print("Connection closed")
    client_socket.close()


# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Start a thread to send audio to the server
sender_thread = threading.Thread(target=audio_sender, args=(client_socket,))
sender_thread.start()

# Wait for the user to press Enter to exit the program
input("Press Enter to exit")

# Clean up
sender_thread.join()
client_socket.close()
stream.stop_stream()
stream.close()
p.terminate()
