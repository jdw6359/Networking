# A simple python server

import socket

# Define Constants HERE
PORT_NUMBER = 12345
MACHINE_TEXT = '[Server] '

print MACHINE_TEXT + 'starting up the server...'

# create a socket object
s = socket.socket()

print MACHINE_TEXT + 'socket created'

# grab the host from the socket
# returns the name of the local machine
host = socket.gethostname()

print MACHINE_TEXT + 'server host: ', host

# reserve a port on our machine for our service
port = PORT_NUMBER

print MACHINE_TEXT + 'about to bind to port: ', port

# bind to the port
s.bind((host, port))

print MACHINE_TEXT + 'bound to ' + host + ' on port: ' + str(port)

# wait for a connection from the client
s.listen(5)

print MACHINE_TEXT + 'server listening........'

while True:
    # establish connection with the client
    c, addr = s.accept()
    
    print MACHINE_TEXT + 'Connection made with ', addr
    
    # send message to client
    c.send('Thank you for connecting')
    
    # close the connection with the client
    c.close()
