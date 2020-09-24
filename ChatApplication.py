import cmd, sys
import socket

class ChatApplicationShell(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = ">> "
		self.intro = "Welcome to Chat Application!"

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
		self.map_ip_to_port = {}

	def postloop(self):
		"""
		Sends a shutdown message to the user.
		Clears up any stateful variable if needed.
		"""
		myip = self.grab_ip()
		if myip in self.map_ip_to_port:
			del self.map_ip_to_port[myip]
		print("Bye!")

	def grab_ip(self):
		return socket.gethostbyname(socket.gethostname())

	def precmd(self, line):
		"""
		Add commands to self._hist variable.
		"""
		if line != '':
			self._hist.append(line.strip())
		if line.isnumeric():
			print(line)
			user_ip = self.grab_ip()
			self.map_ip_to_port[user_ip] = int(line)
		return line

	def do_hist(self, args):
		"""Print a list of commands that have been entered"""
		print(self._hist)

	def do_exit(self, line):
		return -1

	def do_myip(self, line):
		print(self.grab_ip())

	def do_myport(self, line):
		print(self.map_ip_to_port[self.grab_ip()])

	def do_list(self, line):
		print('id: IP address         Port No.')
		f = '{:<2}: {:<15}        {:<5}' #format
		i = 1
		for k in sorted(self.map_ip_to_port.keys()):
			v = self.map_ip_to_port[k]
			print(f.format(*[i, k, v]))

	def do_terminate(self, line):
		if not line.isdigit():
			print("Please enter a positive number to terminate!")
		_id = int(line)
		i = 1
		key_to_delete = ""
		for k in sorted(self.map_ip_to_port.keys()):
			if i == _id:
				key_to_delete = k
				break
			i += 1
		if not key_to_delete:
			print("Please enter a id that is in 'list' command!")
		else:
			del[self.map_ip_to_port[key_to_delete]]
			print("removed connection id %s"%line)

if __name__ == '__main__':
	ChatApplicationShell().cmdloop()
