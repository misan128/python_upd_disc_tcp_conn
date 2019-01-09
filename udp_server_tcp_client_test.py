import threading, queue
import socket
import time

import network_constants

q = queue.Queue()

# client_ip = ""
# client_port = ""

class udpserverThread (threading.Thread):
	def __init__(self, threadID, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = "UDP_SERVER"
		self.queue = queue
	def run(self):
		print("Init " + self.name + " thread")
		# create UDP socket and set it to broadcast
		server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		# Bind the host and port
		server.bind((network_constants.UDP_SERVER_HOST, network_constants.UDP_PORT))
		
		data, udp_server_addr = server.recvfrom(1024)
		print("Received broadcasting from: %s"%str(udp_server_addr))

		self.queue.put(udp_server_addr);

		# Thread execution ends
		print("End " + self.name + " thread")


class tcpclientThread(threading.Thread):
	def __init__(self, threadID, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = "TCP_CLIENT"
		self.queue = queue
	def run(self):
		print("Init " + self.name + " thread")
		# create a TCP/IP socket
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Bind the socket to the port
		client_address = self.queue.get(True)
		print("TCP Client connect to " + client_address[0] + ":" + str(network_constants.TCP_PORT)
		# Listen for incoming connections
		client.connect((client_address[0], network_constants.TCP_PORT))

		try:
			client.sendall(b'tcp_client')
			res = client.recv(1024)
			print("tcp server response: " + str(res))

		finally:
			client.close()
		
		# Thread execution ends
		print("End " + self.name + " thread")





# create new threads
udpserverthread = udpserverThread("Thread-1", q)
tcpclientthread = tcpclientThread("Thread-2", q)

udpserverthread.start()
tcpclientthread.start()

#time.sleep(4)

#q.put(('127.0.0.1', TCP_PORT))

print("Exit Main Thread")