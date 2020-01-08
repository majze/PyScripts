# PyScripts
Useful python scripts for everyday monotonous and repetitive tasks. Why do something more than three times when you can write a script to do it for you?

![Randall Munroe is a beautiful human](https://imgs.xkcd.com/comics/automation.png)
<br>
###### _[Randall Munroe is a beautiful human](https://xkcd.com/)_

## clearSubdirectoriesContents.py
For the specified directory, the script goes into each child subdirectory and delete the contents.

Run intructions:
Navigate to the script location in your favorite terminal and type:
```
py .\clearSubdirectoriesContents.py arg1 arg2 arg3
```

arg1 is mandatory. Enter the custom\directory\path to your top-level folder which contains the subdirectories to be cleared.<br>
arg2 and arg3 are optional and can be entered in any order:

&nbsp; &nbsp; &nbsp; optionalArg2 = del  >> deletes empty directories after clearing their contents<br>
&nbsp; &nbsp; &nbsp; optionalArg3 = skip >> skips the safety check in function verify()

Examples:<br>
```
py .\clearSubdirectoriesContents.py C:\Users\admin\Pictures\gallery del
```
```
py .\clearSubdirectoriesContents.py /home/username/Documents skip del
```

**Q:** Why would you delete directories after clearing their contents? Why not delete the directories right away?<br>
**A:** You can. But I make modifications to this script all the time to leave certain files or directory names alone, and having an exception list in the removeEmpties() function can help.

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
 


[moveUp1]: https://i.imgur.com/42CyxuF.png "moveUp Parent folder"
[moveUp2]: https://i.imgur.com/Q2cF3NF.png "moveUp Child folder"
[moveUp3]: https://i.imgur.com/aU9QT5e.png "moveUp Parent Final State"
