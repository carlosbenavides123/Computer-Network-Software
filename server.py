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
        self.s.listen()
        while True:
            try:
                conn, addr = self.s.accept()
                ip, port = addr
                self.clients[conn] = addr
                print("%s has joined your chat room."%ip)
                Thread(target=self.handle_client, args=(conn, addr)).start()
            except Exception:
                print("Shutting down server...")
                break

    def handle_client(self, client, addr):
        """Handles a single client connection."""
        ip, port = addr
        while True:
            try:
                msg = client.recv(1024).decode()
            except:
                return
            if msg == "connect":
                # initial message for when a client attempts to connect to server
                continue
            broadcast_message = f"\nMessage receieved from: {ip}\nSender's Port: {port}\nMessage: {msg}"
            if msg != "{quit}":
                self.broadcast(broadcast_message.encode())
            else:
                client.send(bytes("{quit} %s %s"%(ip, port), "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(bytes(f"{ip}:{port} has left the {self.host}:{self.port} server!", "utf8"))

    def broadcast(self, msg):
        """Broadcasts a message to all the clients."""
        # print(msg.decode())
        for sock in self.clients:
            sock.send(msg)

    def stop(self):
        self.s.close()
        time.sleep(0.3)
