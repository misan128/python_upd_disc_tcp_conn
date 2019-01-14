import threading
import socket
import time

import network_constants


class tcpserverThread(threading.Thread):
	def __init__(self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = "TCP_SERVE"
	def run(self):
		print("Init " + self.name + " thread")
		# create a TCP/IP socket
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Bind the socket to the port
		server_address = ('', network_constants.TCP_PORT)
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
				conn.sendall(b'HTTP/1.1 200 OK\n\rDate: Mon, 27 Jul 2009 12:28:53 GMT\n\rServer: Apache/2.2.14 (Win32)\n\rLast-Modified: Wed, 22 Jul 2009 19:15:56 GMT\n\rContent-Length: 88\n\rContent-Type: text/html\n\rConnection: Closed\n\r\n\r<html><body><h1>Hello, World!</h1></body></html>')
		finally:
			conn.close()
		
		# Thread execution ends
		print("End " + self.name + " thread")





# create new threads
tcpserverthread = tcpserverThread("Thread-2")

tcpserverthread.start()

print("Exit Main Thread")