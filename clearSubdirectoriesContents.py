# For the specified directory, go into each child subdirectory and delete the contents
# py .\clearSubdirectoriesContents.py custom\directory\path
# optionalArg=del  >> deletes empty directories after clearing their contents
# optionalArg=skip >> skips the safety check in function verify()

import os
import sys
import shutil

def main():
	# original/starting directory
	if (sys.argv[1] != ""):
		origin = sys.argv[1]
	else:
		raise Exception('need path for input')
		# origin = os.path.dirname(os.path.realpath(__file__))

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

if __name__ == "__main__":
	main()