import threading, queue
import socket
import time

import network_constants


q = queue.Queue()

# client_ip = ""
# client_port = ""

class udpclientThread (threading.Thread):
	def __init__(self, threadID, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = "UDP_CLIENT"
		self.queue = queue
		self.num_tx = 5
	def run(self):
		print("Init " + self.name + " thread")
		# create UDP socket and set it to broadcast
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		counter = 0
		check = False


		while not check:
			# try to fetch the client ip from the queue
			try:
				tcp_thread_rx = self.queue.get(True, 1)
			except queue.Empty:
				# if the queue is empty broadcast again
				print("TCP Server not found")
				# currently using loopback network
				# use <broadcast> instead
				# dummy data
				client.sendto(b'hello_world', (network_constants.BROADCAST_ADDR, network_constants.UDP_PORT))
			else:
				# if you got an item from the queue (client ip and port)
				print("TCP Server found")
				print(tcp_thread_rx)
				# check True to break while
				# TODO: eval IP/Port
				check = True
		# Thread execution ends
		print("End " + self.name + " thread")


class tcpserverThread(threading.Thread):
	def __init__(self, threadID, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = "TCP_SERVE"
		self.queue = queue
	def run(self):
		print("Init " + self.name + " thread")
		# create a TCP/IP socket
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Bind the socket to the port
		server_address = (str.encode(socket.gethostbyname(socket.gethostname())), network_constants.TCP_PORT)
		# Listen for incoming connections
		server.bind(server_address);
		server.listen(1)
		# server.settimeout(1)

		# connection waiting loop
		conn, client_addr = server.accept()
		try:
			print('connection from', client_addr)
			data = conn.recv(1024)
			if data:
				print("tcp client req: " + str(data))
				conn.sendall(b'yep')
				self.queue.put(client_addr)
		finally:
			conn.close()
		
		# Thread execution ends
		print("End " + self.name + " thread")





# create new threads
udpclientthread = udpclientThread("Thread-1", q)
tcpserverthread = tcpserverThread("Thread-2", q)

udpclientthread.start()
tcpserverthread.start()

print("Exit Main Thread")