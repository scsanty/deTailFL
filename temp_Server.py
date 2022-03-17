# import socket programming library
import socket
import time

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

# thread function
def threaded(c):
	while True:

		# data received from client
		data = c.recv(1024)
		if not data:
			print('Bye')

			# lock released on exit
			print_lock.release()
			break


		msglen = int(data[:10])
		data = data[10:]
		while len(data) < msglen:
			data += c.recv(1024)
		data = data.decode('utf-8')
		# reverse the given string from client
		data = str(len(data)).ljust(10) + data[::-1]

		data = data.encode('utf-8')

		time.sleep(5)
		# send back reversed string to client
		c.send(data)

	# connection closed
	c.close()


def Main():
	host = ""

	# reverse a port on your computer
	# in our case it is 12345 but it
	# can be anything
	port = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("socket binded to port", port)

	# put the socket into listening mode
	s.listen(5)
	print("socket is listening")

	# a forever loop until client wants to exit
	while True:
		print('Waiting for new connections')
		# establish connection with client
		c, addr = s.accept()

		# lock acquired by client
		print_lock.acquire()
		print('Connected to :', addr[0], ':', addr[1])

		# Start a new thread and return its identifier
		start_new_thread(threaded, (c,))
		print('Triggered thread')
	s.close()


if __name__ == '__main__':
	Main()
