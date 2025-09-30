#!/usr/bin/python3
# netshell.py
# A simple network shell.
import socket, subprocess, select

# create a socket object.
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind it to a port
listener.bind(("", 8080)) # accept from any IP.
# start listening, with a backlog of 10.
listener.listen(10)

# create a list of all sockets, including the listener.
allsocks = [listener]

# loop to do all possible ways of servicing sockets.
while True:
    # which of my sockets are ready to talk?
    ready, output, exceptions = select.select(allsocks, [], [])
    
    for sock in ready:
        # is the socket our listener? If so, accept a new connection
        if sock == listener:
            conn, addr = listener.accept()
            print("New connection from", addr)
            allsocks.append(conn)
        # otherwise, it's an existing client sending a command
        else: 
        	  # recieve the command from the client.
            commbytes = sock.recv(1024) # max size
            if commbytes: # command isn't empty
            	commlist = commbytes.decode().strip().split()
            	print("Recevived command:", commlist)
            try:
                p1 = subprocess.Popen(commlist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p1.communicate()
                response = out + err  # Combine stdout and stderr
            except OSError:
            	 # send the client a "command failed" message
                response = b"Command failed\n"
                
                sock.send(response)
                
