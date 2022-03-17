import socket
import pickle

class Server:
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not isinstance(cls._instance, cls):
			cls._instance = object.__new__(cls)
		return cls._instance

	def __init__(self, headersize = None, function=None, hostname=None, port=None):
		self.HEADERSIZE	= 10 if headersize is None else headersize
		if function is not None:
			self.server_side_func = function
		self.hostname	= socket.gethostname() if hostname is None else hostname
		self.port		= 12345 if port is None else port

	def server_side_func(self, msg):
		print('Nothing to be done from Server end')

	def run_server(self):
		serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serv.connect((self.hostname, self.port))
		serv.listen(5)
		while True:
			clnt, addr = serv.accept()
			print('Connected to :', addr[0], ':', addr[1])
			msg = serv.recv(1024)
			msglen = int(msg[:self.HEADERSIZE])
			msg = msg[self.HEADERSIZE:]
			while len(msg) < msglen:
				msg += serv.recv(1024)
			msg = pickle.loads(msg)
			server_side_func(fullmsg)

		serv.close()
