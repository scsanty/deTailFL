# Import socket module
import socket


def Main():
	# local host IP '127.0.0.1'
	host = '127.0.0.1'

	# Define the port on which you want to connect
	port = 12345

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((host,port))

	# message you send to server
	message = "shaurya says geeksforgeeks"


	#######################################
	import random
	message = ''
	for _ in range(2000):
		message += chr(random.randint(33, 126))
	###################################

	# message sent to server
	message = str(len(message)).ljust(10) + message
	print(message, end='\n\n\n')
	s.send(message.encode('utf-8'))

	# message received from server
	data = s.recv(1024)

	msglen = int(data[:10])
	data = data[10:]
	while len(data) < msglen:
		data += s.recv(1024)

	# print the received message
	# here it would be a reverse of sent message
	print('Received from the server :',str(msglen).ljust(10, ' ') + str(data.decode('utf-8')))

	# close the connection
	s.close()

if __name__ == '__main__':
	Main()
