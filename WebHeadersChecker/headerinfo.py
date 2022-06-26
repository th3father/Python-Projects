import argparse
from matplotlib.pyplot import get
import requests
import urllib.parse

parser = argparse.ArgumentParser(prog='headerinfo.py', usage='python3 headerinfo.py -t <target> -tf <file contianing target list>\n\npython3 headerinfo.py -t https://www.yahoo.com\npython3 headerinfo.py -tf urls.txt')
parser.add_argument('-t', '--target', help='Target ip', required=False)
parser.add_argument('-tf', '--tfile', help='File Containing Target URLs', required=False)
args = parser.parse_args()

#function for getting the headers info
def get_header_info(target):
    parsed_url = urllib.parse.urlsplit(target)
    
    try:
        response = requests.head(target, verify=False)

        #check Strict-Transport-Security
        if(parsed_url.scheme == 'https' and not("Strict-Transport-Security" in response.headers)):
            print("Strict-Transport-Security header does not exist!")

        #check Content-Security-Policy
        if(not("Content-Security-Policy" in response.headers)):
            print("Content-Security-Policy header does not exist!")

        #check X-Frame-Options
        if(not("X-Frame-Options" in response.headers)):
            print("X-Frame-Options header does not exist!")
        
        #check Server
        if(not("Server" in response.headers)):
            print("Server header does not exist!")

        print("All checks preformed successfuly!")
    
    except BaseException:
        print("Could not connect to {}".format(target))

def main():
    #single target mode
    if args.target:
        print("\nSingle ip mode selected.\n")
        print("-------------------------------------------------------------------------------")
        get_header_info(args.target)

    #multi target mode
    elif args.tfile:
        print("\nFile mode selected.\n")
        file = args.tfile
        with open(file, 'r') as target_list:
            for line in target_list.readlines():
                print("-------------------------------------------------------------------------------")
                print("Input IP from file: " + str(line.strip()))
                get_header_info(str(line.strip()))
    
    else:
        print("Wrong usage! use -h to get help.")

if __name__ == '__main__':

    main()