
import socket

class SocketClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.connection = None

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        self.connection = s

    def send_message(self, message):
        if not self.connection:
            self.connect()
        if not self.connection:
            print("Was not able to connect to {self.host} {self.port}")
            return False
        self.connection.sendall(message.encode())
        data = self.connection.recv(1024)
        print(data)
        return True


# connect 192.168.0.178 3233