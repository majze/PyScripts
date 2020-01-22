""" Author: MajZe (D. Spreder) | Language: Python 3.7.4 | Last Edited: Jan 8, 2020
# This script moves all contents of subdirectories up to their parent directory.
  For example, ~/someDir/folder1 , ~/someDir/folder2 , ... , ~/someDir/folderN ,
  and all of the contents of the sub directories brought up to ~/someDir/
# IMPORTANT! Start this script in the top level directory.
# Optional arguments:
    --path full_path
        String - Replace 'full_path' with FULL path to top level directory of ~/someDir
    --verbose
        Boolean - No additional input required
    --rm
        Boolean - No additional input required
# See function argv_init() for more information on arguments
"""

import argparse
import os
import shutil
import sys

def main():
    # argument parser
    parser = argparse.ArgumentParser(description='Optional flags to control script')
    argv_init(parser)
    args = parser.parse_args()
    
    # Original/starting directory
    if args.path:
        origin = args.path
    else:
        origin = os.path.dirname(os.path.realpath(__file__))
        print("\nNo path specified - Default execution path: ", origin)
        # Confirm no path argument if using script file locally
        askConfirm = input("Confirm (y/n): ")
        if askConfirm == "y" or askConfirm == "Y":
            print("Path confirmed, executing...\n")
        elif askConfirm == "n" or askConfirm == "N":
            print("** Job cancelled by user **\n")
            sys.exit()
        else:
            print("Interpreting vague answer as no, stopping script!\n")
            raise Exception("Unexpected user input confirming execution path\n")
    
    # Log path and start of script
    print(f"\nStarting Job in: {origin}")

    # Get list of all subdirectories and log paths
    dirList = [dir for dir in os.listdir(origin) if os.path.isdir(join(origin, dir)) and dir != __file__[2:]]
    print(f"Directories: {dirList}")
    
    # Parse through subdirectories
    for dir in dirList:
        # Current working directory
        cwd = join(origin, dir)
        if args.verbose:
            print("\n", '='*6, f"Parsing {dir}/ ", '='*12)
        
        # Get list of and parse through files in current subdirectory
        fileList = os.listdir(cwd)
        for file in fileList:
            if args.verbose:
                print(f"moving {file}")
            shutil.move(join(cwd, file), origin)

    # Remove empty directories when done, if using --rm argument
    if args.rm:
        print("\n", '='*6, "Removing empties", '='*12)
        for dir in dirList:
            if args.verbose:
                print(f"Removing {dir}")
            os.rmdir(join(origin, dir))
        print("\n** Removed empty directories **")
                
    print("** Operation complete **\n")


def join(path1, path2):
    """Shorthand function for os.path.join()"""
    return os.path.join(path1, path2)


def argv_init(parser):
    parser.add_argument('--path',
                        help='Full path to excute script in')
    parser.add_argument('--verbose', action='store_true',
                        help='Outputs every action to the terminal')
    parser.add_argument('--rm', action='store_true',
                        help='Removes empty directories after moving files')


if __name__ == "__main__":
    main()