## Tiny Syslog Server in Python.
##
## This is a tiny syslog server that is able to receive UDP based syslog
## entries on a specified port and save them to a file.
## That's it... it does nothing else...
## There are a few configuration parameters.

LOG_FILE = 'syslog.log'
HOST, PORT = "192.168.0.151", 6785

#
# NO USER SERVICEABLE PARTS BELOW HERE...
#
import os
import logging
import socketserver

logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

class SyslogUDPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		print('handle')
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		print( "%s : " % self.client_address[0], str(data))
		logging.info(str(data))

def runLogServer():
	print('server start')
	server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
	server.serve_forever(poll_interval=1)


