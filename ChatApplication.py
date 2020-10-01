import cmd, sys
import socket
import bisect

from server import SocketServer
from client import SocketClient

class ChatApplicationShell(cmd.Cmd):
	def __init__(self, port):
		cmd.Cmd.__init__(self)
		self.prompt = ">> "
		self.intro = "Welcome to Chat Application!"
		self.port = port
		self.client_ip = socket.gethostbyname(socket.gethostname())
		if self.client_ip == "127.0.0.1":
			try:
				self.client_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
			except Exception:
				print("Was not able to find a valid client ip...")

		self.connected_remote_hosts = []
		self.map_ip_to_port = {}
		self.map_ip_to_server = {}

		self.create_new_room()
		# self.do_connect(self.client_ip + " " + self.port)

	def create_new_room(self):
		self.client_server = SocketServer(self.client_ip, self.port)

	def do_connect(self, line):
		"""
		Connect to a remote machine.
		connect <remote host, remote port>
		args
		remote host - remote hosts IP
		remote port - remote hosts chat port
		"""
		split_line = line.split(" ")
		if len(split_line) != 2:
			print("Please enter two args only! run 'help connect' for more info.")
		remote_host, remote_port = split_line
		if remote_host in self.map_ip_to_port:
			print("Already connected to %s!"%remote_host)
			return
		bisect.insort_left(self.connected_remote_hosts, remote_host)
		self.map_ip_to_port[remote_host] = remote_port
		self.map_ip_to_server[remote_host] = SocketClient(remote_host, remote_port)

	def default(self, line):
		if line.isdigit():
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
		myip = self.client_ip
		if myip in self.map_ip_to_port:
			del self.map_ip_to_port[myip]
		self.client_server.stop()
		print("Bye!")

	def precmd(self, line):
		"""
		Add commands to self._hist variable.
		"""
		if line != '':
			self._hist.append(line.strip())
		if line.isdigit():
			client_ip = self.client_ip
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
		print(self.client_ip)

	def do_myport(self, line):
		"""Get the port"""
		print(self.map_ip_to_port[self.client_ip])

	def do_list(self, line):
		"""List all the TCP connections you are connected to."""
		print('id: IP address         Port No.')
		f = '{:<2}: {:<15}        {:<5}' #format
		i = 1
		for ip in self.connected_remote_hosts:
			port = self.map_ip_to_port[ip]
			print(f.format(*[i, ip, port]))
			i += 1

	def do_send(self, line):
		"""
		Send a message to a listed connection id.
		For example enter 'list' and see this:
		id: IP address      Port No.
		1   192.xyz.abc.tuv 5432
		2   192.qwe.bvc.ijk 3233
		to send a message to the connection to 192.qwe.bvc.ijk 3233
		enter 'send 2 Hello'
		"""
		split_message = line.split(" ")
		if len(split_message) < 2:
			print("For the send command, please enter two paramters <connection id> <message>, please see 'help send' for more info.")
			return

		connection_id = split_message[0]
		if not connection_id.isdigit() or int(connection_id) <= 0:
			print("For the send command, please enter a valid connection id! (positive integer only!)")
			return
		connection_id = int(connection_id)
		if connection_id > len(self.connected_remote_hosts):
			print("Cannot connect to that!")
			return
		message = ' '.join(split_message[1:])
		if len(message) > 100:
			print("message is too big to send! please enter a shorter message!")
			return
		ip = self.connected_remote_hosts[connection_id - 1]
		remote_server = self.map_ip_to_server[ip]
		if remote_server.send_message(message):
			print("message was sent successfully")
		else:
			print("failed sending message")


	def do_terminate(self, line):
		"""
		Terminate the connection to a listed connection id.
		For example enter 'list' and see this:
		id: IP address      Port No.
		1   192.xyz.abc.tuv 5432
		2   192.qwe.bvc.ijk 3233
		to delete the connection to 192.qwe.bvc.ijk 3233
		enter'teminate 2'
		"""
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
