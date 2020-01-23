""" Author: MajZe (D. Spreder) | Language: Python 3.7.4 | Last Edited: Jan 23, 2020
# For the specified directory, go into each child subdirectory and delete the contents.
# Start this script in the top level directory.
# Input args can accept ignore list of files/folders to keep
# Optional arguments:
    --path full_path
        String - Replace 'full_path' with FULL path to top level directory of ~/someDir
    --ignore string_list
        List - Replace 'string_list' with comma separated values. Include quotes if using spaces.
    --verbose
        Boolean - Logs every I/O operation to the terminal
    --rm
        Boolean - Removes empty subdirectories after deleting their files
    --force
        Boolean - Runs script with no user input, assuming the best intentions. Careful!
"""

import argparse
import os
import shutil
import sys


def main():
    # argument parser
    parser = argparse.ArgumentParser(description='Optional flags that the control script')
    argv_init(parser)
    args = parser.parse_args()
    
    # Original/starting directory
    if args.path:
        origin = args.path
    else:
        origin = os.path.dirname(os.path.realpath(__file__))
        print("\nNo path specified - Default execution path: ", origin)
        # Confirm no path argument if using script file locally
        if args.force:
            print("Forced Path confirmed\n")
        else:
            askConfirm = input("Confirm (y/n): ").casefold()
            if askConfirm == "y":
                print("Path confirmed\n")
            elif askConfirm == "n":
                print("** Job cancelled by user **\n")
                sys.exit()
            else:
                print("Interpreting vague answer as no, stopping script!\n")
                raise Exception("Unexpected user input confirming execution path\n")
    
    # Get ignore list & all subdirectories in origin directory
    if args.ignore:
        ignoreList = getIgnoreList(args)
        print(f"Ignoring files and folders with names: {ignoreList}") 
        dirList = [dir for dir in os.listdir(origin) if os.path.isdir(j(origin, dir)) and dir not in ignoreList]
    else:
        dirList = [dir for dir in os.listdir(origin) if os.path.isdir(j(origin, dir))]
    
    # Safety check before DELETING FILES
    if not args.force:
        verify(dirList, args)
    
    # Parse through subdirectories as main loop
    for dir in dirList:
        # Navigate through subdirectory
        cwd = os.path.join(origin, dir)
        if args.verbose:
            print(f"* Parsing {dir}")
        
        # Gather list of files and folders
        files = [f for f in os.listdir(cwd) if not os.path.isdir(os.path.join(cwd,f))]
        folders = [f for f in os.listdir(cwd) if os.path.isdir(os.path.join(cwd,f))]
        
        # IgnoreList
        if args.ignore:
            files = [f for f in files if f not in ignoreList]
            folders = [f for f in folders if f not in ignoreList]
        
        # Delete all files in subdirectory. Add exceptions here
        for f in files:
            os.remove(j(cwd,f))
            if args.verbose:
                print(f"** Removed {f}")
        
        # Delete all folders in subdirectory. Add exceptions here
        if args.rm:
            for folder in folders:
                shutil.rmtree(j(cwd,folder))
                if args.verbose:
                    print(f"** Removed {folder}")
        
        # Log the directory after having been cleared
        if args.verbose:
            print("* Passed " + dir)
    
    # Remove empty directories
    if args.rm:
        removeEmpties(args, origin, dirList)
        print("Removed empty directories")
    
    print("\n** Operation complete **\n")


def removeEmpties(args, origin, dirList):
    """Removes empty directories"""
    for dir in dirList:
        cwd = j(origin, dir)
        if len(os.listdir(cwd)) == 0:
            os.rmdir(cwd)
            if args.verbose:
                print(f"* Removed empty {dir}")


def verify(dirList, args):
    """Asks user for input before clearing subdirectories"""
    # Check if list is empty
    if len(dirList) == 0:
        print("There are no directories to clear, exiting...")
        raise Exception("dirList is empty")
    
    # Confirm deletion of files
    print('=*='*2, " ABOUT TO CLEAR THE FOLLOWING ", '=*='*4)
    for dir in dirList:
        print(">\t" + dir)
    
    if args.ignore:
        print('=*='*2, " WITH EXCEPTIONS: ", f"{getIgnoreList(args)}")
    print('=*='*2, " CONFIRM Y/N: ", end='')
    answer = input().casefold()
    
    if answer == "y":
        print("Input confirmed")
    elif answer == "n":
        print("Good call. Exiting")
        sys.exit()
    else:
        print("Interpreting vague answer as no, exiting")
        raise Exception("** Job cancelled by user **")


def j(path1, path2):
    """Shorthand function for os.path.join()"""
    return os.path.join(path1, path2)


def getIgnoreList(args):
    """Splits the ignore list by delimiter ',' and returns a list"""
    ignoreList = args.ignore.replace(', ', ',').split(',')
    return ignoreList


def argv_init(parser):
    parser.add_argument('--path',
                        help='Full path to excute script in')
    parser.add_argument('--ignore',
                        help='File extention(s) to ignore')
    parser.add_argument('--rm', action='store_true',
                        help='Removes empty directories after moving files')
    parser.add_argument('--verbose', action='store_true',
                        help='Outputs every I/O action to the terminal')
    parser.add_argument('--force', action='store_true',
                        help='Runs script with no user input')


if __name__ == "__main__":
    main()