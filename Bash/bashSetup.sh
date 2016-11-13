#!/bin/bash

#Prompt user for Windows username and save it
clear
echo -n "Enter your Windows username and press [ENTER]: "
read name

#Ask user if they use a text editor
clear
echo "Enter your the name of your favorite text editor and press [ENTER]"
echo -n "Options are sublime, atom, notepad (why?!) or none: "
read editor


##########################################################
##                  Utility Setup                       ##
##########################################################

#Fix "Unable to resolve host" error
newHost=`cat /etc/hostname`
if [ ! grep -Fxq "$newHost" /etc/hosts ];
then
    echo "
    127.0.0.1   $newHost" >> /etc/hosts
fi

#Disable the stupid ding noise (tab complete)
if [ ! grep -Fxq "set bell-style none" /etc/inputrc ];
then
    echo "#Disable stupid bell ding
    set bell-style none" >> /etc/inputrc
fi

#Disable the stupid ding noise (vim)
if [ ! grep -Fxq "set visualbell" ~/.vimrc ];
then
    echo "set visualbell" >> ~/.vimrc
fi

#Make dev directory
if [ ! -d "/mnt/c/Users/"$name"/dev/" ]; then
  mkdir /mnt/c/Users/"$name"/dev/
fi


##########################################################
##                  Bashrc Config                       ##
##########################################################

#Check if file exists
clear
if [ -f ~/.bashrc ];
then
   echo -n "Overwrite existing bash config? [Y/N]: "
   read prompt
else
   prompt="Y"
fi

#Write it!
if [ $prompt = "Y" ] || [ $prompt = "y" ];
then

rm -f ~/.bashrc

#Custom, user specific config
if [ $editor = "atom" ]; then
customConfig="
#Change start directory
chDir() { cd /mnt/c/Users/"$name"/dev/ ; }
chDir

# Funtion to take parameters and open text editor with said parameters
openEditor() {
  curDir=\${PWD}
  echo \$curDir
  cd /mnt/c/Users/kedvall/AppData/Local/atom/app-1.12.2
  echo \${pwd}
  wstart "$editor".exe "\$\@";
  cd "\$\c\u\r\D\i\r"
}

# Alias to dev folder
alias dev=\"cd /mnt/c/Users/"$name"/dev/\"
alias down=\"cd /mnt/c/Users/"$name"/Downloads/\"
alias exp=\"wstart explorer .\"
alias e=openEditor
"

else
customConfig="
#Change start directory
chDir() { cd /mnt/c/Users/"$name"/dev/ ; }
chDir

# Funtion to take parameters and open text editor with said parameters
openEditor() {
  wstart "$editor".exe "\$@";
}

# Alias to dev folder
alias dev=\"cd /mnt/c/Users/"$name"/dev/\"
alias down=\"cd /mnt/c/Users/"$name"/Downloads/\"
alias exp=\"wstart explorer .\"
alias e=openEditor
"
fi

#Standard config
read -d '' stdConfig <<'EOF'
# Shorten directory
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}[\\033[01;32m\\]\\u\\[\\033[00m\\]:\\[\\033[01;34m\\]\\W\\[\\033[00m\\]\\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\\u:\\W\\$ '
fi

# colored prompt!
PS1='\\e[92;1m\\u@\\h: \\e[96m\\W\\e[0m\\$ '
EOF

#Save this to file
echo "$customConfig" >> ~/.bashrc
echo "$stdConfig" >> ~/.bashrc

#User specified no, don't write it!
else
  echo "Custom config setup skipped"
fi


##########################################################
##                  Package Setup                       ##
##########################################################
#Install packages for development and configure them accouding to CS225 requirements
#apt-get update && apt-get install clang-3.5 libc++abi-dev libc++-dev libpng-dev libsvn-dev gdb valgrind graphviz imagemagick subversion gnuplot git
#update-alternatives --install /usr/bin/clang clang /usr/bin/clang-3.5 100
#update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-3.5 100

#Recompile Valgrind from source
#tar xvjf valgrind-3.11.0.tar.bz2
#cd valgrind-3.11.0
#./configure --prefix = / Usr / local / valgrind-3.11.0
#make -j4
#make install


##########################################################
##                  Final Instructions                  ##
##########################################################
clear
echo "Setup complete!"
echo "Development directory created at C:/Users/"$name"/dev/"
echo "Type dev for dev folder, down for downloads, and exp to open explorer to current dir"
echo "Type edit fileName1 fileName2 fileName3 ... to open editor with specified files"
echo "
Hope you like it! :)"
