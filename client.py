
import socket
import time
from threading import *

class SocketClient(Thread):
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.connection = None
        self.t = None
        self.killed = False

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Attempting to connect to %s:%s..."%(self.host, self.port))
            s.connect((self.host, self.port))
            s.send("connect".encode())
            self.connection = s
            self.t = Thread(target=self.receive, args=(s,))
            self.t.start()
            return True
        except:
            pass
        return False


    def receive(self, client_socket, own_ip=None, own_port=None):
        while True:
            msg = client_socket.recv(1024).decode()
            if msg.startswith("{quit}"):
                _, ip, port = msg.split(" ")
                if ip == own_ip and own_port == port:
                    client_socket.close()
                    break
            else:
                if not msg:
                    break
                print(msg)
        if self.killed:
            raise SystemExit()

    def send_message(self, message):
        if not self.connection:
            self.connect()
        if not self.connection:
            print("Was not able to connect to {self.host} {self.port}")
            return False
        self.connection.sendall(message.encode())
        return True

    def close(self, own_ip, own_port):
        if self.t:
            try:
                self.t.killed = True
                self.send_message("{quit}")
                self.t.join()
            except:
                print("Error occured attempting to kill the thread.")
                return False
        if self.connection:
            try:
                self.connection.close()
            except:
                print("Error occured attempt to close the connection to remote host...")
                return False
        print(f"Successfully closed connection to {self.host}:{self.port}")
        return True
