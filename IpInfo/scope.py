import argparse
import geocoder
import socket
import pytz
from datetime import datetime
import ipaddress

parser = argparse.ArgumentParser(prog='scope.py', usage='python3 scope.py -t <target> -tf <file contianing target list> -c <CIDR> -cf <file containing CIDRs list>\n\npython3 scope.py -t 8.8.8.8\npython3 scope.py -tf ips.txt')
parser.add_argument('-t', '--target', help='Target ip', required=True)
parser.add_argument('-tf', '--tfile', help='File Containing Target URLs/IPs', required=False)
parser.add_argument('-c', '--cidr', help='CIDR block', required=False)
parser.add_argument('-cf', '--cfile', help='File Containing Target CIDR blocks', required=False)
args = parser.parse_args()

# the function for getting the ip info and writing them to the output stream.
def get_ip_info(target):
    try:
        target_ip = socket.gethostbyname(target)
        target_info = geocoder.ip(target_ip)

        print("IP: " + target_ip)
        print("Owner: " + target_info.org)
        print("Country: " + target_info.country)
        print("State/Province: " + target_info.state)
        print("City: " + target_info.city)
        print("ZipCode: " + target_info.postal)
        print("Lat/Lng: " + str(target_info.lat) + "/" + str(target_info.lng))
        print("TimeZone: " + target_info.raw["timezone"])
        print("Current time at target location: " + str(datetime.now(pytz.timezone(target_info.raw["timezone"]))))
    
    except BaseException:
        print("Error: target {} is not a valid target".format(target))

# the function for getting the ip list in each CIDR block. 
def get_CIDR_info(target):
    try:
        for ip in ipaddress.IPv4Network(target):
                print("-------------------------------------------------------------------------------")
                get_ip_info(str(ip))
    
    except BaseException as err:
        print(target)
        print(err)
        print("Error: {} is not a valid CIDR!".format(target))


def main():
    if args.target:
        print("\nSingle ip mode selected.\n")
        print("-------------------------------------------------------------------------------")
        get_ip_info(args.target)
        
        print("-------------------------------------------------------------------------------")

    elif args.tfile:
        print("\nFile mode selected.\n")
        file = args.tfile
        with open(file, 'r') as target_list:
            for line in target_list.readlines():
                print("-------------------------------------------------------------------------------")
                print("Input IP from file: " + str(line.strip()))
                get_ip_info(str(line.strip()))
        
        print("-------------------------------------------------------------------------------")

    elif args.cidr:
        print("\nCIDR mode selected.\n")
        get_CIDR_info(str(args.cidr))
      
        print("-------------------------------------------------------------------------------")

    elif args.cfile:
        print("\nCIDR file mode selected.\n")
        file = args.cfile
        with open(file, 'r') as target_list:
            for line in target_list.readlines():
                print("-------------------------------------------------------------------------------")
                print("input CIDR from file: " + line.strip())
                get_CIDR_info(line.strip())
    
        print("-------------------------------------------------------------------------------")

    else:
        print("Wrong usage! use -h to get help.")


if __name__ == '__main__':

    main()
        

    


