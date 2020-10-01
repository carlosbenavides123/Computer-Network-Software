
import socket

class SocketClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            data = s.recv(1024)
        print('received', repr(data))

    def send_message(self, message):
        if not self.connection:
            self.connect()
        if not self.connection:
            print("Was not able to connect to {self.host} {self.port}")
            return False
        self.connection.sendall(b'message')
        return True


