import socket
import threading
import time
import config
from modules.exceptions import EmptyMessageException

class ChatServer:

    def __init__(self):
        # Configuration for the Server
        self.ADDR = (socket.gethostbyname(socket.gethostname()), config.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        # Config Values
        self.PORT = config.PORT
        self.HEADER = config.HEADER
        self.FORMAT = config.FORMAT
        self.DISCONNECT_MESSAGE = config.DISCONNECT_MESSAGE

    # Handle Incoming Client Connections and Message Decoding
    def handle_client(self, conn, addr):
        print(f"[+] {self.ADDR} connected")
        connected = True
        while connected:
            msg_length = conn.recv(config.HEADER).decode(config.FORMAT)

            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(config.FORMAT)
                if msg == config.DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[-] {addr} connection closed")
                    return "closed"
            else:
                raise EmptyMessageException(f"{msg}")
            print(f"[+] {self.ADDR}: {msg}")

    # Run the Server and put every Client in their own Thread
    def run(self):
        self.server.listen()
        print(f"[+] Server is listening on {self.ADDR}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[+] Threads: {threading.activeCount() - 1}")
