#!/bin/bash

# ------------------------------------------------------------------
# - Filename: install.sh
# - Author: draed
# - Dependency: None
# - Description: shell script to install doctum_helper on debian
# - Creation date: 2025-02-20
# - Bash version: 5.2.15(1)-release
# ------------------------------------------------------------------

####################################################
#                    Parameters
####################################################

DOCTUM_HELPER_BIN_PATH_DEFAULT=${DOCTUM_HELPER_BIN_PATH_DEFAULT:-"bin/doctum_helper"}
DOCTUM_HELPER_PATH_SRC=${DOCTUM_HELPER_PATH_SRC:-"./src"}
DOCTUM_HELPER_ALIAS_DEFAULT=${DOCTUM_HELPER_ALIAS_DEFAULT:-"dh"}
DOCTUM_HELPER_WRAPPER_PATH="$HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT/src/doctum_helper_wrapper.sh"


####################################################
#               utils function
####################################################

create_alias_in_bashrc() {
### Create alias in bashrc ###
    ALIAS_NAME=$1
    ALIAS_COMMAND=$2
    ## Check if the alias already exists 
    if ! grep -q "alias $ALIAS_NAME=" $HOME/.bashrc; then
        echo "alias $ALIAS_NAME='$ALIAS_COMMAND'" >> $HOME/.bashrc
        echo "Alias '$ALIAS_NAME' added to .bashrc."
        source $HOME/.bashrc
    else
        echo "Alias '$ALIAS_NAME' already exists in .bashrc."
    fi
}

####################################################
#               main install function
####################################################

## copy doctum helper src to bin path
mkdir -p $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT
cp -r $DOCTUM_HELPER_PATH_SRC $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT

## configure python dependencies using venv
virtualenv $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT/venv
source $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT/venv/bin/activate
python -m pip install -r $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT/src/requirements.txt
deactivate

## fix exec rights for wrapper
chmod +x $DOCTUM_HELPER_WRAPPER_PATH

## try to create link to user bin folder (might fail for specifics linux distrib)
ln -s $DOCTUM_HELPER_WRAPPER_PATH /usr/$DOCTUM_HELPER_BIN_PATH_DEFAULT 2>/dev/null
if [ $? -ne 0 ];then
    ## other method to call script that has lesser chance to fail
    create_alias_in_bashrc $DOCTUM_HELPER_ALIAS_DEFAULT
fi
