# Move all contents of subdirectories up to parent directory in python.
# For example, ~/someDir/folder1 , ~/someDir/folder2 , ... , ~/someDir/folderN 
# and all of the contents of the sub directories brought up to ~/someDir/
# IMPORTANT!!! This script assumes ~/someDir/ ONLY contains subdirectories.
# Move all extra files out so ~/someDir/ only includes this script and the sub directories

import shutil
import os
import sys

# original/starting directory
odir = os.path.dirname(os.path.realpath(__file__))

# current working directory
cwd = os.getcwd()

# grab all subdirectories
dir_list = os.listdir(odir)

# exclude this script file from directory list
try:
	file = __file__[2:]
	dir_list.remove(file)
except:
	print("Problem moving python script file")

# parse through subdirectories
for dir in dir_list:
	cwd = os.path.join(odir,dir)
	print("Parsing", dir + "/", " ====================")
	
	# parse through files in current subdirectory
	file_list = os.listdir(cwd)
	for file in file_list:
		print("moving ", file)
		shutil.move(os.path.join(cwd,file), odir)

# remove empty directories when done
answer = input("\nRemove " + str(list(dir_list)) + " directories as well? y/n ")
if (answer == 'y' or answer == 'Y'):
	for dir in dir_list:
		os.rmdir(os.path.join(odir,dir))
	print("Removed empty directories")
		
print("Operation complete!")