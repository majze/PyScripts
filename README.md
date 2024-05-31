# PyScripts
Useful python scripts for everyday monotonous and repetitive tasks.<br>
Why do something more than three times when you can write a script to do it for you?

![Randall Munroe is a beautiful human](https://imgs.xkcd.com/comics/automation.png)
<br>
###### _[Randall Munroe is a beautiful human](https://xkcd.com/)_

## clearSubdirectoriesContents.py
For the specified directory, the script goes into each child subdirectory and delete the contents.<br>

For example, every folder in ~/parentDir/ will be parsed and have its content deleted, unless specified using the ignoreList passed into the argument '--ignore'. All the files and folders inside each subdirectory ~/parentDir/folder1 , ... , ~/parentDir/folderN etc will be removed unless an exception is made.<br>

### Run Instructions
Navigate to the script location in your favorite terminal and type:
```
py .\clearSubdirectoriesContents.py
```
Runinng without any arguments will run the script LOCALLY, and will prompt the user twice: Once to confirm the script's run location, and again to confirm the subdirectories to be cleared. It does not matter what the files or folders are named, as long as they do not include nonstandard characters.<br>

Start this script in the top level directory, either by using the '--path' argument or placing the script file there. <br>
### Optional arguments: <br>
&nbsp;&nbsp;--path **full_path** *(String)* <br>
```
py .\clearSubdirectoriesContents.py --path full_path
```
&nbsp;&nbsp;&nbsp;&nbsp;Replace **full_path** with the full path to top level directory of ~/someDirectory <br>
&nbsp;&nbsp;&nbsp;&nbsp;*e.g.* /home/MyUsername/bad_selfies


&nbsp;&nbsp;--ignore **ignore_list** *(String)*<br>
```
py .\clearSubdirectoriesContents.py --ignore ignore_list
```
&nbsp;&nbsp;&nbsp;&nbsp;Replace **ignore_list** with comma separated values. Include quotes if using spaces. <br>
&nbsp;&nbsp;&nbsp;&nbsp;*e.g.* backups,saves,secrets


&nbsp;&nbsp;--verbose <br>
&nbsp;&nbsp;&nbsp;&nbsp;**Boolean** - Logs every I/O operation to the terminal. No additional input required <br>

&nbsp;&nbsp;--rm <br>
&nbsp;&nbsp;&nbsp;&nbsp;**Boolean** - Removes empty subdirectories after deleting their files, unless specified by the --ignore argument.<br>

&nbsp;&nbsp;--force <br>
&nbsp;&nbsp;&nbsp;&nbsp;**Boolean** - Runs script with no user input, assuming the best intentions. Careful! <br><br>

### Examples:
```
py .\clearSubdirectoriesContents.py --ignore .git,node_modules,src --verbose
```
```
py .\clearSubdirectoriesContents.py --path /home/username/Documents --ignore 'plex, My Games' --rm --force
```

**Q:** Why delete empty directories *after* removing their content? Why not delete the directories right away? <br>
**A:** This script was made with exceptions in mind, so some files and folders can be left untouched. There's not really a point to running this script with --rm and without --ignore. Just delete the directories manually in that case.

## moveFilesUpOneLevel.py
This script moves all contents of subdirectories up to their parent directory. This script is nonrecursive, but can be modified to handle additional levels of directories. Be careful when moving all files and folders up if there are any files that share the same name. <br> <br>
For example, ~/someDir/folder1 , ~/someDir/folder2 , ... , ~/someDir/folderN , and all of the contents of the sub directories brought up to ~/someDir/ <br>


#### Starting file structure
![moveUp1] &nbsp; ![moveUp2]

#### Final file structure
![moveUp3] <br>
It does not matter what the files or folders are named, as long as they do not include nonstandard characters.

### Run Instructions
Start this script in the top level directory, either by using the '--path' argument or placing the script file there. <br> <br>
Optional arguments: <br>
&nbsp;&nbsp;--path *full_path* <br>
&nbsp;&nbsp;&nbsp;&nbsp;**String** - Replace *full_path* with FULL path to top level directory of ~/someDir <br>
&nbsp;&nbsp;--verbose <br>
&nbsp;&nbsp;&nbsp;&nbsp;**Boolean** - Logs every read/write operation to the terminal. No additional input required <br>
&nbsp;&nbsp;--rm <br>
&nbsp;&nbsp;&nbsp;&nbsp;**Boolean** - Removes empty subdirectories after moving files up. No additional input required <br> <br>
See function argv_init() for more information on arguments

Examples:<br>
```
py .\moveFilesUpOneLevel.py
```
```
py .\moveFilesUpOneLevel.py --path 'C:\Users\admin\Documents\someDir' 
```
```
py .\moveFilesUpOneLevel.py --path 'C:\Users\admin\Documents\someDir' --verboose --rm
```

## fileSizer.py
Needs updating. Not native OS friendly.
 




## CompressionTest.ps1
Suprise! It's a PowerShell script. This script runs through four different compression methods using 7-zip, to get a better idea of which is best for your specific needs. If space is your only issue, Ultra compression is probably best. If waiting for the heat death of the universe is an issue, perhaps losing a few megabits is worth the time saved. Use this if you need to know what's best for your specific server environment and the types/number of files you are compressing.

Change the paths at the top of the script to match your environment. The current setup will create various zip files from within a specific directory of your choosing, log the time it took for each operation, and after a set amount of runs, finish the log file with an average for each compression level. So far it tests using mx5, mx7, mx9, and LZMA - but you can always add more switches. Learn more about [7z switches here](https://sevenzip.osdn.jp/chm/cmdline/switches/method.htm).

While LZMA is better with more available memory and cores, it actually takes much longer on production environments with shared resources - one more reason to test compression levels using the actual environment instead of your personal workstation.

[moveUp1]: https://i.imgur.com/42CyxuF.png "moveUp Parent folder"
[moveUp2]: https://i.imgur.com/Q2cF3NF.png "moveUp Child folder"
[moveUp3]: https://i.imgur.com/aU9QT5e.png "moveUp Parent Final State"
