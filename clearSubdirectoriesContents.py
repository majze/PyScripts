""" Author: MajZe (D. Spreder) | Language: Python 3.7.4 | Last Edited: Jan 8, 2020
# For the specified directory, go into each child subdirectory and delete the contents.
# Start this script in the top level directory.
TODO:
# Optional arguments:
    --path full_path
        String - Replace 'full_path' with FULL path to top level directory of ~/someDir
    --verbose
        Boolean - No additional input required
    --rm
        Boolean - No additional input required
# See function argv_init() for more information on arguments
"""
# 
# py .\clearSubdirectoriesContents.py custom\directory\path
# optionalArg=del  >> deletes empty directories after clearing their contents
# optionalArg=skip >> skips the safety check in function verify()

import argparse
import os
import shutil
import sys
from colorama import init, Fore
init()

def main():
    # argument parser
    parser = argparse.ArgumentParser(description='Optional flags to control script')
    argv_init(parser)
    args = parser.parse_args()
    
###
	#FIXME:
    print(getIgnoreList(args))
    sys.exit()
    
    # Original/starting directory
    if args.path:
        origin = args.path
    else:
        origin = os.path.dirname(os.path.realpath(__file__))
        print("\nNo path specified - Default execution path: ", origin)
        # Confirm no path argument if using script file locally
        askConfirm = input(f"{Fore.CYAN}Confirm (y/n): {Fore.RESET}")
        if askConfirm == "y" or askConfirm == "Y":
            print("Path confirmed, executing...\n")
        elif askConfirm == "n" or askConfirm == "N":
            print(f"{Fore.RED}** Job cancelled by user **{Fore.RESET}\n")
            sys.exit()
        else:
            print(f"{Fore.YELLOW}Interpreting vague answer as no, stopping script!{Fore.RESET}\n")
            raise Exception(f"{Fore.RED}Unexpected user input confirming execution path{Fore.RESET}\n")

    # Get all subdirectories in origin directory
    dirList = os.listdir(origin)
    
    # Safety check before DELETING FILES
    if len(sys.argv) > 2 and "skip" in sys.argv:
        pass
    else:
        verify(dirList)
    
    # Parse through subdirectories as main loop
    for dir in dirList:
        
        # Navigate through subdirectory and gather list of files and folders
        cwd = os.path.join(origin, dir)
        files = [f for f in os.listdir(cwd) if not os.path.isdir(os.path.join(cwd,f))]
        folders = [f for f in os.listdir(cwd) if os.path.isdir(os.path.join(cwd,f))]
        
        # Delete all files in subdirectory. Add exceptions here
        for file in files:
            os.remove(os.path.join(cwd,file))
        
        # Delete all folders in subdirectory. Add exceptions here
        for folder in folders:
            shutil.rmtree(os.path.join(cwd,folder))
        
        # Log the directory after having been cleared
        print("\tCleared " + dir)
    
    # Remove empty directories. Useful if exceptions above exist
    if len(sys.argv) > 2 and "del" in sys.argv:
        removeEmpties(origin, dirList)
    
    print("** Operation complete **\n")

def removeEmpties(origin, dirList):
    """Removes empty directories"""
    for dir in dirList:
        os.rmdir(os.path.join(origin, dir))
    print("\tRemoved empty directories")
    
def verify(dirList):
    """Asks user for input before clearing subdirectories"""
    print("\n" + "="*12 + " ABOUT TO CLEAR THE FOLLOWING " + "="*12)
    
    for dir in dirList:
        print("\t" + dir)
    
    print("="*17 + " ARE YOU SURE? Y/N " + "="*18)
    answer = input()
    
    if answer == "y" or answer == "Y":
        print("Confirmed")
    elif answer == "n" or answer =="N":
        print("Good call. Exiting")
        sys.exit()
    else:
        print("Interpreting vague answer as no, exiting")
        raise Exception("** Job cancelled by user **")
###

def join(path1, path2):
    """Shorthand function for os.path.join()"""
    return os.path.join(path1, path2)


def getIgnoreList(args):
    """Splits the ignore list by delimiter ',' and returns a list"""
    ignoreList = args.ignore.replace(' ', '').split(',')
    print(f"Ignoring files with substrings: {ignoreList}")
    return ignoreList

def argv_init(parser):
    parser.add_argument('--path',
                        help='Full path to excute script in')
    parser.add_argument('--ignore',
                        help='File extention(s) to ignore')
    parser.add_argument('--rm', action='store_true',
                        help='Removes empty directories after moving files')
    parser.add_argument('--verbose', action='store_true',
                        help='Outputs every action to the terminal')


if __name__ == "__main__":
    main()