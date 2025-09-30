CPSC 42700 Project 2: Building a Python botnet
Michael Wallin
March 23, 2025

NAME
	netshell.py, botinstall.py, candc.py
	
USAGE
	./netshell.py 
	./botinstall.py
	./candc.py

	
DESCRIPTION
	This program uses a botnet controlled by the command and control user (you) to quickly gain access to a system and execute commands 
	
COMMAND-LINE OPTIONS
    no command line is used for this botnet.

INPUT FILE FORMAT
	for compromised_hosts.txt
	[IP Address] [Username] [Password]
	
	example: 10.0.2.11 usera abc123

KNOWN BUGS AND LIMITATIONS
	Cannot attack systems with strong password protection or any passwords that aren't "baseball, adf, or abc123"
	
	only can do attacks on port 8080
	
ADDITIONAL NOTES
		I was not able to get the C&C portion to run correctly, the bots would execute a ls command but would not print the 
		results of the ls command.
		
		However my program still works if one or more of my Debian 6 machines is down.
