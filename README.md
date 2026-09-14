# PyScripts
Useful python scripts for everyday monotonous and repetitive tasks.<br>
Why do something more than three times when you can write a script to do it for you?

![Randall Munroe is a beautiful human](https://imgs.xkcd.com/comics/automation.png)
<br>
###### _[Randall Munroe is a beautiful human](https://xkcd.com/)_

## dir_purge.py
Deletes all files within all child sub-directories existing in a top-level directory.

For a given parent directory, the script traverses each immediate sub-directory and deletes its contents. Exclusions can be specified via the `--ignore` argument.

### Run Instructions
Execute the script from the terminal. If no `--path` is provided, it defaults to the directory where the script resides. The script prompts for path confirmation and deletion confirmation unless forced.

```bash
./dir_purge.py
```

### Arguments
*   `--path <full_path>`: Target top-level directory.
*   `--ignore <ignore_list>`: Comma-separated list of file or folder names to exclude. Use quotes for names containing spaces.
*   `--verbose`: Outputs all I/O actions to the terminal.
*   `--rmtree`: Removes origin directories entirely after clearing contents.
*   `--force`: Bypasses all user confirmation prompts.

### Examples
```bash
./dir_purge.py --ignore .git,node_modules,src --verbose
./dir_purge.py --path /home/username/Documents --ignore "plex, My Games" --rmtree --force
```

### Performance Note: The Fast Purge Update
When the script executes with `--rmtree` and without any `--ignore` constraints, it triggers a "fast purge." Instead of parsing through a directory file-by-file in Python to unlink them individually, it passes the directory directly to the OS via `shutil.rmtree`. This eliminates iteration overhead and significantly improves performance on drives with high file counts. The standard item-by-item deletion method is only utilized when exclusions must be respected.
 
## moveFilesUpOneLevel.py
This script moves all contents of sub-directories up to their parent directory. This script is nonrecursive, but can be modified to handle additional levels of directories. Be careful when moving all files and folders up if there are any files that share the same name. <br> <br>
For example, ~/someDir/folder1 , ~/someDir/folder2 , ... , ~/someDir/folderN , and all of the contents of the sub directories brought up to ~/someDir/ <br>


#### Starting file structure
![moveUp1] &nbsp; ![moveUp2]

#### Final file structure
![moveUp3] <br>
It does not matter what the files or folders are named, as long as they do not include nonstandard characters.

### Run Instructions
Navigate to the script location in your favorite terminal and type:
```
py .\moveFilesUpOneLevel.py
```
Start this script in the top level directory, and it will run LOCALLY. Or use the '--path' argument to specify another location. <br> <br>

### Optional arguments: <br>
&nbsp;&nbsp;--path **full_path** *(String)* <br>
```
py .\moveFilesUpOneLevel.py --path full_path
```
&nbsp;&nbsp;&nbsp;&nbsp;Replace **full_path** with the full path to top level directory of ~/someDirectory <br>
&nbsp;&nbsp;&nbsp;&nbsp;*e.g.* /home/MyUsername/Pictures/Vacations <br> <br>

&nbsp;&nbsp;--verbose <br>
&nbsp;&nbsp;&nbsp;&nbsp;Logs every I/O operation to the terminal. No additional input required. <br> <br>

&nbsp;&nbsp;--rm <br>
&nbsp;&nbsp;&nbsp;&nbsp;Removes empty subdirectories after moving files up. No additional input required. <br> <br>
See function argv_init() for more information on arguments <br> <br>

### Examples:<br>
```
py .\moveFilesUpOneLevel.py --path 'C:\Users\admin\Documents\someDir' 
```
```
py .\moveFilesUpOneLevel.py --path 'C:\Users\admin\Documents\someDir' --verboose --rm
```

## fileSizer.py
Needs updating. Not native OS friendly. <br> <br>
 




## CompressionTest.ps1
Suprise! It's a PowerShell script. This script runs through four different compression methods using 7-zip, to get a better idea of which is best for your specific needs. If space is your only issue, Ultra compression is probably best. If waiting for the heat death of the universe is an issue, perhaps losing a few megabits is worth the time saved. Use this if you need to know what's best for your specific server environment and the types/number of files you are compressing.

Change the paths at the top of the script to match your environment. The current setup will create various zip files from within a specific directory of your choosing, log the time it took for each operation, and after a set amount of runs, finish the log file with an average for each compression level. So far it tests using mx5, mx7, mx9, and LZMA - but you can always add more switches. Learn more about [7z switches here](https://sevenzip.osdn.jp/chm/cmdline/switches/method.htm).

While LZMA is better with more available memory and cores, it actually takes much longer on production environments with shared resources - one more reason to test compression levels using the actual environment instead of your personal workstation.

[moveUp1]: https://i.imgur.com/42CyxuF.png "moveUp Parent folder"
[moveUp2]: https://i.imgur.com/Q2cF3NF.png "moveUp Child folder"
[moveUp3]: https://i.imgur.com/aU9QT5e.png "moveUp Parent Final State"
