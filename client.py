
import socket
from threading import *

class SocketClient(Thread):
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.connection = None

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        self.connection = s
        Thread(target=self.receive, args=(s,)).start()

    def receive(self, client_socket):
        while True:
            msg = client_socket.recv(1024).decode()
            if msg == "{quit}":
                client_socket.close()
                break
            if not msg:
                break
            print(msg)

    def send_message(self, message):
        if not self.connection:
            self.connect()
        if not self.connection:
            print("Was not able to connect to {self.host} {self.port}")
            return False
        self.connection.sendall(message.encode())
        # data = self.connection.recv(1024)
        # print(data)
        return True


# connect 192.168.0.178 3233