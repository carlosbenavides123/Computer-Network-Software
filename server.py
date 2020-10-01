import socket, time
from threading import *
from multiprocessing import *

class SocketServer(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.host = host
        self.port = int(port)
        self.killed = False
        self.start()

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        while True:
            try:
                conn, addr = self.s.accept()
                print("Connected to %s"%addr)
                message = conn.recv(1024)
                conn.sendall(message)
                print(message)
            except:
                print("Shutting down server...")
                break

    def stop(self):
        self.s.close()
        time.sleep(1)
