import cmd, sys
import socket

from server import SocketServer
from client import SocketClient

class ChatApplicationShell(cmd.Cmd):
	def __init__(self, port):
		cmd.Cmd.__init__(self)
		self.prompt = ">> "
		self.intro = "Welcome to Chat Application!"

		self.client_ip = socket.gethostbyname(socket.gethostname())
		self.port = port

		self.connected_remote_hosts = [self.client_ip]
		self.map_ip_to_port = {self.client_ip: port}

		self.create_new_room()
		self.do_connect(self.client_ip, self.port)

	def create_new_room(self):
		self.client_server = SocketServer(self.client_ip, self.port)

	def do_connect(self, remote_host, remote_port):
		"""
		Connect to a remote machine.
		args
		remote host - remote hosts IP
		remote port - remote hosts chat port
		"""
		if remote_host in self.map_ip_to_port:
			print("Already connected to %s!"%remote_host)
			return
		self.client = SocketClient(remote_host, remote_port)
		self.connected_remote_hosts = bisect.insort_left(self.connected_remote_hosts, remote_port)
		self.map_ip_to_port[remote_host] = remote_port

	def default(self, line):
		if line.isnumeric():
			print("Connecting to port %s"%line)
		else:
			print("Unrecognized command %s, please enter 'help' for help!"%line)

	def preloop(self):
		"""
		Initialize history and other stateful variables.
		"""
		cmd.Cmd.preloop(self)
		self._hist = []

	def postloop(self):
		"""
		Sends a shutdown message to the user.
		Clears up any stateful variable if needed.
		"""
		myip = self.grab_ip()
		if myip in self.map_ip_to_port:
			del self.map_ip_to_port[myip]
		print("Bye!")

	def precmd(self, line):
		"""
		Add commands to self._hist variable.
		"""
		if line != '':
			self._hist.append(line.strip())
		if line.isnumeric():
			client_ip = self.grab_ip()
			self.map_ip_to_port[client_ip] = int(line)
		return line

	def do_hist(self, args):
		"""Print a list of commands that have been entered"""
		print(self._hist)

	def do_exit(self, line):
		"""Exit the application"""
		return -1

	def do_myip(self, line):
		"""Get my ip"""
		print(self.grab_ip())

	def do_myport(self, line):
		"""Get the port"""
		print(self.map_ip_to_port[self.grab_ip()])

	def do_list(self, line):
		"""List all the TCP connections you are connected to."""
		print('id: IP address         Port No.')
		f = '{:<2}: {:<15}        {:<5}' #format
		i = 1
		for ip in self.connected_remote_hosts:
			port = self.map_ip_to_port[ip]
			print(f.format(*[i, ip, port]))

	def do_terminate(self, line):
		"""Terminate the program."""
		if not line.isdigit():
			print("Please enter a positive number to terminate!")
		_id = int(line)

		i = 1
		key_to_delete = ""
		for ip in self.connected_remote_hosts:
			if i == _id:
				key_to_delete = ip
				break
		if not key_to_delete:
			print("Please enter a id that is in 'list' command!")
		else:
			del[self.map_ip_to_port[key_to_delete]]
			self.connected_remote_hosts.remove(key_to_delete)
			print("removed connection id %s"%line)

if __name__ == '__main__':
	print('Number of arguments:', len(sys.argv), 'arguments.')
	print('Argument List:', str(sys.argv))
	port = sys.argv[1]
	ChatApplicationShell(port).cmdloop()
