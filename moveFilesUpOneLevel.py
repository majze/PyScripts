# Move all contents of subdirectories up to their parent directory.
# For example, ~/someDir/folder1 , ~/someDir/folder2 , ... , ~/someDir/folderN 
# and all of the contents of the sub directories brought up to ~/someDir/
# IMPORTANT!!! This script assumes ~/someDir/ ONLY contains subdirectories.
# After moving all files, ~/someDir/ only includes this script and the sub directories

# Arguments must be entered in correct order as seen below:
# optionalArg1=parentPath >> path: points the script towards the parent path instead of running locally
# optionalArg2=removeEmpties >> Boolean: { {True,true,1}, {False,false,0} } for removeEmpties logic
# If using optionalArg2, you MUST use optionalArg1 first. Working on modularizing this.

import shutil
import os
import sys

def main():

	# Get and parse optional args
	# Original/starting directory
	origin = ""
	if len(sys.argv) > 1:
		if ("\\" in sys.argv[1]) or ("/" in sys.argv[1]):
			origin = sys.argv[1]
		else:
			print("\nWARNING: Bad path or missing path. Start script in default location?")
			origin = os.path.dirname(os.path.realpath(__file__))
			print("Default location: ", origin)
			
			# Confirm no path argument if using script file locally
			askConfirm = input("Enter y/n: ")
			if askConfirm == "y" or askConfirm == "Y":
				print("Confirmed path, starting job\n")
			elif askConfirm == "n" or askConfirm == "N":
				print("** Job cancelled by user **\n")
				sys.exit()
			else:
				print("\nInterpreting vague answer as no, stopping script\n")
				raise Exception("** Unexpected input for askConfirm **\n")
	else:
		origin = os.path.dirname(os.path.realpath(__file__))
	
	# Confirm and log optionalArg1=parentPath
	print("\n** Starting Job **\nLocation: {}".format(origin))
	
	# Remove empty subdirectories when finished?
	removeEmpties = True
	if len(sys.argv) > 2:
		commandArgs = [['true', '1'], ['false', '0']]
		if sys.argv[2].casefold() in commandArgs[0]:
			removeEmpties = True
			print("Remove subdirectories after moving files: True\n")
		elif sys.argv[2].casefold() in commandArgs[1]:
			removeEmpties = False
			print("Remove subdirectories after moving files: False\n")
		else:
			print("Bad input for optionalArg2=removeEmpties, exiting\n")
			sys.exit()
	
	# Current working directory
	cwd = os.getcwd()

	# Get list of all subdirectories
	dirList = [dir for dir in os.listdir(origin) if dir != __file__[2:]]

	# Parse through subdirectories
	for dir in dirList:
		cwd = os.path.join(origin, dir)
		print("Parsing", dir + "/", " ====================")
		
		# Get list of and parse through files in current subdirectory
		fileList = os.listdir(cwd)
		for file in fileList:
			print("moving ", file)
			shutil.move(os.path.join(cwd, file), origin)

	# Remove empty directories when done, if removeEmpties == True
	if removeEmpties:
		for dir in dirList:
			os.rmdir(os.path.join(origin, dir))
		print("** Removed empty directories **\n")
				
		print("** Operation complete! **\n")

if __name__ == "__main__":
	main()