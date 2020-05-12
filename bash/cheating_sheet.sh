#!/bin/bash

# Clear the screen
clear

# echo -e: enable special characters with backslash
# echo -n: do not add new line in the end

# Running date
echo "Starting program at $(date)"

# Print out information
# Difference between echo and printf:
# + both of them are Bash built-in commands.
# - echo: exits with 0 status, prints with an end of line
# - printf: allow formatting string, exits with non-zero upon failure
echo "Running program $0 with $# arguments with pid $$"
echo

# Find the command path
echo "\$ which echo"
which echo
echo

# Show current path
echo "\$ pwd"
pwd
echo

# cut the $PATH to multiple lines by ':'
# tr: translate character to new one
# echo $PATH | tr ':' '\n'

# ls: list files and folders
# cd -: cd to previous folder

# folder permissions:
# o refer to:
#   https://www.hackinglinuxexposed.com/articles/20030424.html
#   https://unix.stackexchange.com/questions/21251/execute-vs-read-bit-how-do-directory-permissions-in-linux-work
# o r: ability to list (ls) all the files in the directory
# o w: delete, create and rename files in the directory, useless if x is not set
# o x: right to enter into the directory (cd to it), and to access its files and subfolders

# rmdir: remove directories only if they are empty

# ctrl+l: clean screen and move to top, same as "clear"

# use cat as cp:
# E.g., copy a.txt to b.txt:
# $ cat < a.txt > b.txt

# tee: read input and write to a file and screen

# change backlight brightness by command:
#   $ cd /sys/class/backlight/intel_backlight
#   $ sudo su
#   # echo 100 > brightness
# You can also do it in this way:
#   $ echo 100 | sudo tee brightness

# "": expand the variables after $
# '': pure string

# $USER
echo "Hello, $USER"
echo

echo "Today's date is `date`, this is week `date +"%V"`."
echo

echo "These users are currently connected:"
w | cut -d " " -f 1 - | grep -v USER | sort -u
echo

echo "This is `uname -s` running on a `uname -m` processor."
echo

echo "This is the uptime information:"
uptime
echo

# Function
# $0: script name
# $1 - $9: arguments
# $@: all the arguments starting from $1
# $_: last argument in the previous command, including $0
# $?: exit status of previous command
# !!: previous command
mdcd () {
  mkdir -p "$1"
  cd "$1"
}

# true: return the error code 0
# false: return the error code 1
# a && b: execute b only if a has an exit status zero
# a || b: execute b only if a has an exit status non-zero

# process substitution:
# Put the output of "ls" and "ls .." together and write to screen
# $ cat <(ls) <(ls ..)

# $(command): execute command and return its output,
#             a modern synonym for `command`
echo "This is in $(pwd)"

# [[ is bash's improvement of [.
# Bash conditional expression:
# https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html#Bash-Conditional-Expressions

# {}: extend the groups separated by comma
# create folders foo and bar and then touch foo/a, foo/b, foo/c, bar/a, bar/b, bar/c
mkdir {foo,bar}
touch {foo,bar}/{a,b,c}

# if you are not sure about the exact path of python, use "env"
# #!/usr/bin/env python
# This kind of line in the beginning is called "shebang"

# tldr: a man page with practical usages of commands
# homepage for tldr-bash-client: https://gitlab.com/pepa65/tldr-bash-client

# find: search files
# -name: name patter
# -iname: case insensative -name
# -type: f for file, d for directory
# -mtime: modification time, -7 for modified in the last 7 days
# -exec: excecute command for the found files {}
# $ find . -name *.py -type f

# locate: find files quickly from the file system database
# updatedb: update the database manually, may need sudo

# ctrl+r: back search history commands, press ctrl+r repeatedly will cycle among these commands

# sed
# $ echo 'abcaba' | sed 's/\(ab\)*//g'
# or
# $ echo 'abcaba' | sed -E 's/(ab)*//g'
# since sed is old, so use '-E' to use modern expression patterns

# awk
# $ awk 'BEGIN { rows = 0 } $1 == 1 && $2 ~ /^c.*e$/ { rows += 1 } END {print rows }'
# set rows to 0 in the beginning,
# search everyline with first column is 1 and second column matches ^c.*e$,
# then rows add 1,
# in the end, print rows

# Test your regular expressions at: https://regex101.com/
# (): capture group
# (?:): non-capture group
# \1, \2, ...: get the match of capture groups, (aa|bb) only the last one is captured
# *: 0 or more, greedy
# *?: 0 or more, non-greedy

# sort: sort the list
# uniq: only show unique values

# paste: merge lines into one line
# Join all the lines into a single line, using the specified delimiter:
# $ paste -s -d delimiter file
# Similar as above, use ',' as delimiter.
# $ paste -sd, file

# bc -l: simple calculator

# xargs
# Run a command using the input data as arguments:
# arguments_source | xargs command

# journalctl: show log information
# $ sudo journalctl

echo "The End."
