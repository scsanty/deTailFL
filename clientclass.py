import socket
import pickle

class Client:
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not isinstance(cls._instance, cls):
			cls._instance = object.__new__(cls)
		return cls._instance

	def __init__(self, headersize = None, function=None, hostname=None, port=None):
		self.HEADERSIZE	= 10 if headersize is None else headersize
		if function is not None:
			self.client_side_func = function
		self.hostname	= socket.gethostname() if hostname is None else hostname
		self.port		= 12345 if port is None else port

	def client_side_func(self, msg):
		print('Nothing to be done from Client end')

	@self.run_client
	def send_to_server(self, msg):
		# TODO: Sanity check
		msg = pickle.dumps(msg)
		msg = bytes(str(len(msg)).ljust(self.HEADERSIZE), 'utf-8') + msg
		return msg

	def run_client(self, func):
		def wrapper(*args, **kwargs):
			clnt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clnt.connect((self.hostname, self.port))
			msg = func(*args, **kwargs)
			clnt.send(msg)

			msg = s.recv(1024)
			msglen = int(msg[:10])
			msg = msg[10:]
			while len(msg) < msglen:
				msg += clnt.recv(1024)
			clnt.close()

			msg = pickle.loads(msg)
			return msg

		return wrapper
