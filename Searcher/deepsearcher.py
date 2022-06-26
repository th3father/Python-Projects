import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(prog='''deepsearcher.py', usage='python3 deepsearcher.py -st <search type> -td <target directory> -fn <filenames> -sl <strings list> -e <extensions> -r <recursion> \n
                                                                  python3 deepsearcher.py -td .\n
                                                                  python3 deepsearcher.py -td . -e txt,py\n
                                                                  python3 ipinfo.py -t myfile.txt -s''')
parser.add_argument('-st', '--searchtype', help='''Searches the directory for 1:\tSearches for file names in the target directory (use --filenames to input custom list of file names to search and --extlist to customize file extensions)
                                                                          2:\tSearches for \"username\",\"password\", and \"apikey\" in every file of target directory (use --stringlist to customize strings to search for and --extlist to customize file extensions).''',default=0, required=True, type=int)
parser.add_argument('-td', '--targetdir', help='Target directory.', required=True)
parser.add_argument('-fn', '--filenames', help='List of filenames to search for.(Comma separated)', required=False)                                                                                  
parser.add_argument('-sl', '--stringlist', help='List of strings to search for.(Comma separated)', required=False)                                                                                  
parser.add_argument('-e', '--extlist', help='List of file extensions.(Comma separated)', required=False)
parser.add_argument('-r', '--recursive', help='Searches recursively in the subdirectories.', required=False, action='store_true')
args = parser.parse_args()

#reads each file and searches for the strings
def search_contents(file_path, strings_list):
    file = open(file_path, 'r')
    for target_line in file:
        for string in strings_list:
            if string in target_line:
                print("-" * 50)
                print("Found {} in {}".format(string, file.name))
                print(target_line + "\n")

def main():
    #list of sensitive strings
    target_strings={'password',
                'username',
                'apikey'}

    #list of sensitive file names
    target_file_names={'password.txt',
                   'web.config',
                   'sitelist.xml'}

    #list of extensions:
    target_extensions={'txt', 'doc', 'docx', 'xls', 'xlsx'}

    if args.searchtype == 1:
        print("\n")
        print("Searching ...")

        #update filenames list
        if args.filenames:
            target_file_names = args.filenames.split(",")

        #update extensions list
        if args.extlist:
            target_extensions = args.extlist.split(",")

        #find paths to search
        paths = []
        if args.recursive:
            for path in Path(args.targetdir).rglob('*.*'):
                paths.append(os.path.abspath(path))
                        
        else:
            files = os.listdir(args.targetdir)
            for target_file in files:
                if os.path.isfile(target_file):
                    paths.append(os.path.abspath(target_file))

        for path_to_file in paths:
            basename = os.path.basename(path_to_file)

            already_printed = []
            for name in target_file_names:
                for ext in target_extensions:
                    if ((name in basename) or ((name + '.' + ext)==basename)):
                        if path_to_file in already_printed:
                            break
                        print("Found an important file: {}\n".format(path_to_file))
                        already_printed.append(path_to_file)

        print("Search ended!")

    elif args.searchtype == 2:
        print("\n")
        print("Searching ...")

        #update extensions list
        if args.extlist:
            target_extensions = args.extlist.split(",")

        #update strings list
        if args.stringlist:
            target_strings = args.stringlist.split(",")

        #find paths to search
        paths = []
        if args.recursive:
            for path in Path(args.targetdir).rglob('*.*'):
                paths.append(os.path.abspath(path))
                
        else:
            files = os.listdir(args.targetdir)
            for target_file in files:
                if os.path.isfile(target_file):
                    paths.append(os.path.abspath(target_file))

        for path_to_file in paths:            
            if (os.path.splitext(path_to_file)[1].replace('.', '')) in target_extensions:
                search_contents(path_to_file, target_strings)
            
        print("Search ended!")

    else:
        print("Wrong usage! use -h to get help.")


if __name__ == '__main__':

    main()