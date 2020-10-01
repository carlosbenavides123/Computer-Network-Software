
import socket

class SocketClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(b'hello word')
            data = s.recv(1024)
        print('received', repr(data))
