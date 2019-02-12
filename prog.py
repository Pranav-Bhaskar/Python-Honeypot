#!/usr/bin/python3
import socket
import sys
import _thread
import datetime

logfile = './Requests.log'

def getHostname():
	global hostname, IPAddr
	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname(hostname)
	print('Hostname : ' + hostname)
	print('IP : ' + IPAddr)
	print('Port : ' + str(Port))
	
def saviour(data, currentDT, metaData):
	header = ('<request datetime="' + str(currentDT) + '" clientIP="' + metaData[0] +
		 '" clientPortNumber="' + str(metaData[1]) + '">\n')
	footer = '\n</request>\n'
	with open(logfile, 'a+') as f:
		f.write(header)
		f.write(data)
		f.write(footer)

def getData(conn):
	data = b''
	while True:
		byte = conn.recv(1024)
		if byte == b'':
			break
		data += byte
	return data

def getRequest(conn, metaData):
	print('Got a connection from : ' + metaData[0] + ':' + str(metaData[1]))
	byteData = getData(conn)
	conn.close()
	try:
		data = byteData.decode()
	except:
		data = str(byteData)[2:-1]
	currentDT = datetime.datetime.now()
	saviour(data, currentDT, metaData)

def waitForRequest():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((IPAddr, Port))
		sock.listen(20)
	except PermissionError:
		print('Error : Not enough permitions to bind to Port ' + str(Port))
		sock.close()
		return
	except:
		print('Error : Couldnot bind socket')
		return
	
	try:
		print('Send a KeyboardInterrupt to termiante the program')
		while(True):
			c, md = sock.accept()
			_thread.start_new_thread(getRequest, (c, md))
	except KeyboardInterrupt:
		sock.close()
		print('Server closed.')
	except:
		print('UnexpectedError : Closing server')
		sock.close()

if __name__ == '__main__':
	global Port
	if len(sys.argv) is not 2:
		print('Usage : ' + sys.argv[0] + ' <Port_Number>')
		sys.exit()
	try:
		Port = int(sys.argv[1])
	except ValueError:
		print('Usage : ' + sys.argv[0] + ' <Port_Number>')
		sys.exit()
	getHostname()
	waitForRequest()
	sys.exit()
