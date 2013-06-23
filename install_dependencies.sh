#!/bin/sh
# Kevin Xu / imkevinxu
# 2012.08.23

# Basic script to install all the dependencies for Django Project Builder
# Tested on a Mac OSX 10.7 (Lion) and 10.8 (Mountain Lion)

PYTHON_VERSION=`python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'`

# Adds GCC ARCHFLAGS if none detected
if [ -z "$ARCHFLAGS" ]
    then
        echo "export ARCHFLAGS='-arch i386 -arch x86_64'" >> ~/.bash_profile
fi

# Installing pip, distribute, django, virtualenv, virtualenvwrapper
if [ -z `which pip` ]
    then
        echo "Installing pip..."
        sudo easy_install pip
fi

# Installs Distribute http://pypi.python.org/pypi/distribute
curl -O http://python-distribute.org/distribute_setup.py
sudo python distribute_setup.py
rm -f distribute*

if [ -z `which django-admin.py` ]
    then
        echo "Installing django..."
        sudo pip install django
fi

if [ -z `which virtualenv` ]
    then
        echo "Installing virtualenv..."
        sudo pip install virtualenv
fi

if [ -z `which virtualenvwrapper.sh` ]
    then
        echo "Installing virtualenvwrapper..."
        sudo pip install virtualenvwrapper
fi

# Adds lines to the shell startup file so that virtualenvwrapper can work
# http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file
if [ -z "$WORKON_HOME" ]
    then
        echo "Adding virtualenvwrapper variables to ~/.bash_profile"
        echo source `which virtualenvwrapper.sh` >> ~/.bash_profile
        source `which virtualenvwrapper.sh`
fi

# Fixes problem that occurs on OSX 10.7 Lion when making a new virtualenv,
# it goes looking for disutils but crashes if it can't find one
# http://stackoverflow.com/questions/3129852/python-cant-locate-distutils-path-on-mac-osx
if [ `echo $PYTHON_VERSION | grep -c "2.7" ` -gt 0 ]
    then
        sudo touch /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/distutils/__init__.py
fi

# Detects if the user has git installed and prompts them to install it if not
if [ -z `which git` ]
    then
        echo
        echo "[WARNING] Detected git has not been installed"
        echo "INSTALL git here http://git-scm.com/downloads"
fi

echo
echo "    ヽ(^o^)丿  yaaaaaaaay"
echo
echo "    All dependencies installed!"
echo "    If there are still errors, try installing Xcode and then Command Line Tools"
echo "    http://stackoverflow.com/questions/11170414/how-to-get-virtualenv-to-work-after-upgrading-to-lion"
