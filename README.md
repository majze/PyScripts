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
Move all contents of subdirectories up to their parent directory. For example: <br>

#### Starting file structure
![moveUp1] &nbsp; ![moveUp2]

#### Final file structure
![moveUp3]

#### IMPORTANT!!!
This script assumes parent folder ~/someDir/ ONLY contains subdirectories. After moving all files, ~/someDir/ only includes this script and the sub directories if desired. <br> <br>
If using optionalArg2, you MUST use optionalArg1 first. Working on modularizing this for next version. <br> <br>
Optional Arguments must be entered in correct order as listed below: <br>
1. This script can be run locally in the parent folder with no arguments, OR:
2. optionalArg1=parentPath >> path: points the script towards the parent path instead of running locally <br>
3. optionalArg2=removeEmpties >> Boolean: { {True,true,1}, {False,false,0} } for removeEmpties logic <br>

Examples:<br>
```
py .\moveFilesUpOneLevel.py
```
```
py .\moveFilesUpOneLevel.py C:\Users\admin\Documents\someDir 
```
```
py .\moveFilesUpOneLevel.py C:\Users\admin\Documents\someDir False
```

## fileSizer.py
Needs updating. Not native OS friendly.
 


[moveUp1]: https://i.imgur.com/42CyxuF.png "moveUp Parent folder"
[moveUp2]: https://i.imgur.com/Q2cF3NF.png "moveUp Child folder"
[moveUp3]: https://i.imgur.com/aU9QT5e.png "moveUp Parent Final State"
