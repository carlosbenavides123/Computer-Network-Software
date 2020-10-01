
import socket
from threading import *

class SocketServer(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.host = host
        self.port = int(port)
        self.start()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            while conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    print(data)
                    if not data:
                        break
                    conn.sendall(data)
        print("ended server")
