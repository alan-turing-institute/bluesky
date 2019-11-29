#!/bin/bash

# Check for python3. 
# NOTE: Uses `which` as `command` test method fails in certain environments.
if [[ `which python3  &>/dev/null | wc -l` -gt 0]]; then
    printf "Found python3\n"
else
    printf "Please install python3\n"
    exit 1
fi

# Check for pip3.
if [[ `which python3 -m pip | wc -l` -gt 0 ]]; then
    printf "Found pip3\n"
else
    printf "Please install python3-pip\n"
    exit 1
fi

# Translate long options to short
# See https://stackoverflow.com/questions/402377/using-getopts-in-bash-shell-script-to-get-long-and-short-command-line-options
for arg
do
    delim=""
    case "$arg" in
       --headless) args="${args}-h ";;
       # pass through anything else
       *) [[ "${arg:0:1}" == "-" ]] || delim="\""
           args="${args}${delim}${arg}${delim} ";;
    esac
done
# Reset the translated args
eval set -- $args

# Parse the options
headless=false
requirements="requirements.txt"
venvname="venv"
while getopts ":he:" opt; do
  case $opt in
    h)
      printf "Headless mode installation\n"
      headless=true
      requirements="requirements_headless.txt"
      ;;
    e)
      printf "Virtual environment name: $OPTARG\n"
      venvname=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -e $venvname ]; then
    printf "Virtual environment %s already exists.\nPlease remove or specify a different name via option -e.\n" $venvname
    exit 1
fi

# matplotlib imports tkinter
python3 -c "import tkinter"
status=$?
if [[ $status != 0 ]]; then
    printf "Please install python3-tk\n"
    exit 1
fi

# Create a virtual environment.
# NOTE: Fallback to python3's inbuilt venv if virtualenv fails
printf "Creating virtual environment: $venvname\n"
(python3 -m pip install --upgrade virtualenv && \
  virtualenv -p python3 $venvname) || \
    (python3 -m venv $venvname) || (
        printf "Please install virtualenv\n" && \
        exit 1
    )

printf "Activating virtual environment\n"
source $venvname/bin/activate

printf "Installing dependencies\n"
python3 -m pip install -r $requirements

status=$?
if [[ $status != 0 ]]; then
    printf "Failed to install dependencies.\n"
    exit 1
fi

# If running on a mac, apply this matplotlib fix:
# https://markhneedham.com/blog/2018/05/04/python-runtime-error-osx-matplotlib-$
if [[ $(uname -s) == Darwin ]]; then
    file=$HOME/.matplotlib/matplotlibrc
    if [ ! -e $file ]; then
        printf "Adding ~/.matplotlib/matplotlibrc\n"
        echo "backend: TkAgg" >> $HOME/.matplotlib/matplotlibrc
    fi
fi

printf "Installation successful\n"
printf "To run BlueSky"
if [ "$headless" = true ] ; then
     printf "in headless mode"
fi
printf ":\n"
printf "> source $venvname/bin/activate\n"
printf "> python BlueSky.py"
if [ "$headless" = true ] ; then
     printf " --headless"
fi
printf "\n"
