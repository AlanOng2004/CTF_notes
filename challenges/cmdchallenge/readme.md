**This is my playthrough of the Command Challenge.**
**Link**: https://cmdchallenge.com
**Objective**: Learn basic commands lines for Linux

**Chal 1: Ways to print in terminal**

echo <text>
printf <text>

More about echo:
echo -n <text>: prints a new line after text

**Chal 2: Print current working directory**

pwd

**Chal 3: List names of files in current directory**

ls

**Chal 4: Print contents of file in current directory**

cat <filename>

**Chal 5: Print the last 5 lines of a file**

tail -n 5 <file>
tail -5 <file>

tail -n: prints new line after command

**Chal 6: Create empty file in current directory**

touch <file>

**Chal 7: Create directory named tmp/files in current directory**

Hint: The directory "tmp/" does not exist, one command is needed to create both "/tmp" and "/tmp/files"

mkdir -p tmp/files: -p creates any directory if it does not exist, else, do nothing

mkdir tmp tmp/files 
mkdir tmp && mkdir tmp/files

**Chal 8: Copy a file to another directory**

cp <file> <directory>

**Chal 9: Move a file to another directory**

mv <file> <directory>

**Chal 10: Create a symbolic link that points to a file**

Symbolic Link (symlink) is a type of file in Linux that points to another file or folder on your computer. Kind of like shortcuts. They are also called soft links.

Soft links are similar to shortcuts, and can point to another file or directory in any file system.

Hard links are also shortcuts for files and folders, but a hard link cannot be created for a folder or file in a different file system.

ln -s <path_to_file/folder_to_be_linked> <path_of_link_to_be_created or name of new_file>
-s specifies that link should be soft.

**Chal 11: Delete all the files in the directory; including all subdirs**

Hint: There are files and directories that start with a dot ".", "rm -rf *" won't work here!

rm -rf {*,.*}
-r recurses through directories
-f forces the deletion
{*,.*} indicates to check even the files with , or . headers

**Chal 12: Remove all files with a specific extension name in current directory**

find . -type f -name "<extension>" -delete

**Chal 13: There is a file named access.log in the current working directory. Print all lines in this file that contains the string "GET".**

cat access.log | grep "GET"

**Chal 14: Print all files in current directory (just filename) that contain the string "500"**

ls | grep -lr "500"

grep -l means files with match

**Chal 15: Print file paths for all <filenames> in current directory**

find . -type f -name <name>

**Chal 16: Print all matching lines (without the filename or the file path) in all files under the current directory that start with "access.log" that contain the string "500".**

grep -r -h "500"

grep -r means do not print filenames

**Chal 17: Extract all IP addresses from files that start with "access.log" printing one IP address per line.**

grep -ro ^[0-9.]*

-o means output the parts of the line that match the pattern

^ is the start of a line
[0-9.] matches any digits or dots
* matches zero or more of the preceeding characters

**Chal 18: Count the number of files in the current working directory. Print the number of files as a single integer.**

ls -l | wc -l

ls -l means long format
wc means word count and -l means the number of lines

**Chal 19: Print the contents of access.log sorted.**

cat access.log | sort

**Chal 20: Print the number of lines in access.log that contain the string "GET".**

cat access.log | grep "GET" | wc -l

**Chal 21: The file split-me.txt contains a list of numbers separated by a ; character. Split the numbers on the ; character, one number per line.**

cat <file> | tr ";" "\n"

tr <replace> <newthing>

**Chal 22: Print the numbers 1 to 100 separated by spaces.**

echo {1..100}

{1..100} is a brace expression, it generates a sequence of numbers from 1 to 100. It works with letters too!

echo{1..10..1} the 3rd number indicates the steps

echo(01..05} will add 0 to the front

**Chal 23: This challenge has text files (with a .txt extension) that contain the phrase "challenges are difficult". Delete this phrase from all text files recursively.**

find . -name "*txt" -type f -exec sed -i 's/challenges are difficult//g' {} \;

-exec: executes whatever after the -exec command
sed -i 's/ ... / ... /g': sed is the stream editor, -e edits the files in place
s/stuff_to_replace/new_stuff/g

{} is a placeholder in find which gets replaced by the current file name that find found.

\; ends the -exec command.

**Chal 24: The file sum-me.txt has a list of numbers, one per line. Print the sum of these numbers.**

jq -s add <file>

jp is a command line tool for processing JSON
-s reads all JSON objects from the input into a single array
add adds lmao

 
