import os

def main():
	# files to ignore
	ignore = ["readme.txt", "fileSizer.py", "log.txt"]
	# size in MB to alert
	threshold = 4000

	odir = os.getcwd()
	dir_list = os.listdir(odir)
	for x in ignore:
		try:
			dir_list.remove(x)
			os.remove("log.txt")
		except:
			pass


	for dir in dir_list:
		cwd = os.path.join(odir, dir)
		files = [file for file in os.listdir(cwd)]
		sizes = [(file, os.path.getsize(cwd+"\\"+file)/1000//1000) for file in files if os.path.getsize(cwd+"\\"+file)/1000//1000 > 20]
		print(sizes)
		alert(sizes, threshold)

# flip sign in if-statement to see files larger or smaller than threshold
def alert(size, threshold):
	if size[0][1] > threshold:
		log = open("log.txt", "a+")
		log.write(str(list(size))+"\n")
		log.close()
		
if __name__ == "__main__":
	main()
