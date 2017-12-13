import socket
import sys

host = str(sys.argv[1])
port = 9020
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = (host, port)
sock.connect(server_address)

data = sock.recv(4096)
print data

while data != "adios\r\n":
        message = raw_input('AaronClient>>>> ')
        sock.sendall(message + "\r\n")
        data = sock.recv(4096)
        print data


print >> sys.stderr, 'exiting chat server'
sock.close()
