#!/bin/bash

# Clear the screen
clear

# Print out information
# Difference between echo and printf:
# + both of them are Bash built-in commands.
# - echo: exits with 0 status, prints with an end of line
# - printf: allow formatting string, exits with non-zero upon failure
echo "This is information provided by mysystem.sh. Program starts now."

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

echo "The End."
