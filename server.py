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
        self.clients = {}

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        while True:
            try:
                conn, addr = self.s.accept()
                ip, port = addr
                self.clients[conn] = addr
                print("Connected to %s"%ip)
                Thread(target=self.handle_client, args=(conn, addr)).start()
            except Exception:
                print("Shutting down server...")
                break

    def handle_client(self, client, addr):  # Takes client socket as argument.
        """Handles a single client connection."""
        ip, port = addr
        while True:
            msg = client.recv(1024).decode()
            broadcast_message = f"\nMessage receieved from: {ip}\nSender's Port: {port}\nMessage: {msg}"
            if msg != bytes("{quit}", "utf8"):
                self.broadcast(broadcast_message.encode())
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]
                # broadcast(bytes("%s has left the chat." % , "utf8"))
                break

    def broadcast(self, msg, prefix=""):  # prefix is for name identification.
        """Broadcasts a message to all the clients."""
        print(msg.decode())
        for sock in self.clients:
            sock.send(msg)

    def stop(self):
        self.s.close()
        time.sleep(0.3)
