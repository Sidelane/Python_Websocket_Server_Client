import socket
import config

class ChatClient():

    def __init__(self):
        # Open the Websocket to connect to the Server
        try:
            self.ADDR: tuple = (config.SERVER, config.PORT)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
        except ConnectionRefusedError:
            print(f"[-] Couldnt connect to {self.ADDR}")
        

    def send_header(self, msg_len: int):
        try:
            send_length = str(msg_len).encode(config.FORMAT)
            send_length += b' ' * (config.HEADER - len(send_length))
            self.client.send(send_length)
        except OSError:
            print(f"[-] Couldnt connect to {self.ADDR}")

    def send(self, msg):
        try:
            message = msg.encode(config.FORMAT)
            self.send_header(len(message))
            self.client.send(message)
        except OSError:
            print(f"[-] Couldnt connect to {self.ADDR}")

    def get_user_input(self):
        want_to_send = True

        while want_to_send:
            print("> ", end="")
            inp = input()
            if inp == "!byebye":
                self.disconnect()
                want_to_send = False
            else:
                self.send(inp)

    def disconnect(self):
        try:
            msg = "!byebye"
            message = msg.encode(config.FORMAT)
            self.send_header(len(message))
            self.client.send(message)
        except OSError:
            print(f"[-] Couldnt connect to {self.ADDR}")
