# A simple python client

import socket

# Define Constants Here
PORT_NUMBER = 12345
MACHINE_TEXT = '[Client] '

print MACHINE_TEXT + 'starting up the client...'

# create a socket object
s = socket.socket()

print MACHINE_TEXT + 'socket created'

# grab the host from the socket
# returns the name of the local machine
host = socket.gethostname()

print MACHINE_TEXT + 'client host: ', host

# reserve a port on our machine for our service
port = PORT_NUMBER

print MACHINE_TEXT + 'about to connect to server'

s.connect((host, port))
print MACHINE_TEXT + 'connected to server'

# Receive message from server
print s.recv(1024)

# close the connection to server
print MACHINE_TEXT + 'closing connection to server...'
s.close()
