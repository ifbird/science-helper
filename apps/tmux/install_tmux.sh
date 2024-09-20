#!/bin/bash

# Refer to: https://gist.github.com/sudkumar/6062def9d56d946b98b6a3853093ee74
#
# Installing tmux locally
#
# 1. visit: https://github.com/tmux/tmux
# 2. create a local directory to install tmux
# 3. download depencencies
#     1. libevent
#         1. visit: http://libevent.org/
#         2. download the stable version
#     2. ncurses
#         1. visit: http://invisible-island.net/ncurses/
#         2. download the stable version
#     3. tmux
#         1. visit: https://github.com/tmux/tmux/releases
#         2. download the stable .tar.gz
# 4. install all the dependencies first and last tmux by running following commands
#
#   tar xvf [--file--.tar.gz]
#   cd [---file--]
#   ./configure --prefix=$HOME/local CPPFLAGS="-P"
#   make
#   make install
#
# 5. `export PATH="$HOME/local/bin:$PATH"` into your bashrc file

rm -rf tmux_temp_installation_dir 2> /dev/null
mkdir tmux_temp_installation_dir
cd tmux_temp_installation_dir
pwd

# Download necessary libraries libevent and ncurses
echo "Please visit http://libevent.org/ and copy the latest stable version's .tar.gz url"
echo "Paste URL"
read libeventurl
wget $libeventurl -O libevent.tar.gz

echo "Please visit http://invisible-island.net/ncurses/ and copy the latest stable version's .tar.gz url"
echo "Paste URL"
read ncursesurl
wget $ncursesurl -O ncurses.tar.gz

# Download tmux
echo "Please visit https://github.com/tmux/tmux/releases and copy the latest stable version's .tar.gz url"
echo "Paste URL"
read tmuxurl
wget $tmuxurl -O tmux.tar.gz

# echo "Installing tmux into your ~/.local/bin/tmux"


# In CSC Puhti we need to load gcc
module load gcc/9.1.0


# Install packages
function installPackage {
  # $1 holds tar.gz

  # Delete temp install dir if it exists
  rm -rf temp_install_dir 2> /dev/null

  # Create a temp folder to untar the packages
  mkdir temp_install_dir

  # Untar the package
  # --strip-components=1: only keep the first component of the folder,
  # e.g., libevent-2.1-table --> libevent
  tar xvf $1 -C temp_install_dir --strip-components=1

  # Enter the folder
  cd temp_install_dir

  # Configure, make and make install
  # -P: do not include linemarkers in the precompiled versions, not necessary
  ./configure --prefix=$HOME/local CPPFLAGS="-P"
  make -j 8
  make install
  cd ..
}


echo "Installing libevent..."
installPackage libevent.tar.gz

echo "Installing ncurses..."
installPackage ncurses.tar.gz

echo "Installing tmux..."
installPackage tmux.tar.gz


# Append following line to your .zshrc or .bashrc or .bash_profile file
# export PATH="$HOME/local/bin:$PATH"
