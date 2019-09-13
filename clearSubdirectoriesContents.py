# For the specified directory, goes into each child subdirectory and delete the contents
# py .\clearSubdirectoriesContents.py custom\directory\path
# optionalArg=del  >> deletes empty directories after clearing their contents
# optionalArg=skip >> skips the safety check in function verify()

import os
import sys
import shutil

def main():
	# original/starting directory
	if (sys.argv[1] != ""):
		odir = sys.argv[1]
	else:
		raise Exception('need path for input')
		# odir = os.path.dirname(os.path.realpath(__file__))

	# current working directory
	cwd = os.getcwd()

	# grab all subdirectories
	dir_list = os.listdir(odir)
	
	# safety check before DELETING FILES
	if len(sys.argv) > 2 and "skip" in sys.argv:
		pass
	else:
		verify(dir_list)
	
	# parse through subdirectories
	for dir in dir_list:
		cwd = odir + "\\" + dir
		files = [f for f in os.listdir(cwd) if not os.path.isdir(os.path.join(cwd,f))]
		folders = [f for f in os.listdir(cwd) if os.path.isdir(os.path.join(cwd,f))]
		
		for file in files:
			os.remove(os.path.join(cwd,file))
		
		for folder in folders:
			shutil.rmtree(os.path.join(cwd,folder))
		
		print("\tCleared " + dir)
	
	if len(sys.argv) > 2 and "del" in sys.argv:
		removeEmpties(odir, dir_list)
	
	print("** Operation complete **\n")

def removeEmpties(odir, dir_list):
	"""Removes empty directories"""
	for dir in dir_list:
		os.rmdir(odir + "\\" + dir)
	print("\tRemoved empty directories")
	
def verify(dir_list):
	"""Asks user for input before clearing"""
	print("\n" + "="*12 + " ABOUT TO CLEAR THE FOLLOWING " + "="*12)
	for dir in dir_list:
		print("\t" + dir)
	print("="*12 + " ARE YOU SURE? Y/N " + "="*23)
	answer = input()
	if answer == "y" or answer == "Y":
		print("Confirmed")
	elif answer == "n" or answer =="N":
		print("Good call. Exiting")
		sys.exit()
	else:
		print("Interpreting vague answer as no, exiting")
		raise Exception("** Job cancelled by user **")
		sys.exit()

if __name__ == "__main__":
	main()