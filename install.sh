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
    ## force using latest value
    unalias $ALIAS_NAME &>/dev/null
    if ! grep -q "alias $ALIAS_NAME=" $HOME/.bashrc; then
        echo "alias $ALIAS_NAME='$ALIAS_COMMAND'" >> $HOME/.bashrc
        echo "Alias '$ALIAS_NAME' added to .bashrc."
    else
        echo "Alias '$ALIAS_NAME' already exists in .bashrc."
    fi
}

add_env_to_bashrc() {
### Add env to bashrc ###
    ENV_VAR_NAME=$1
    ENV_VAR_VALUE=$2
    if ! grep -q "export $ENV_VAR_NAME=" $HOME/.bashrc; then
        echo "export $ENV_VAR_NAME='$ENV_VAR_VALUE'" >> $HOME/.bashrc
        echo "Var '$ENV_VAR_NAME' added to .bashrc."
    else
        echo "Var '$ENV_VAR_NAME' already exists in .bashrc."
    fi
}

####################################################
#               main install function
####################################################

## copy doctum helper src to bin path
mkdir -p $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT
cp -r $DOCTUM_HELPER_PATH_SRC $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT

## configure python dependencies using venv
virtualenv $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT/venv &>/dev/null
source $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT/venv/bin/activate &>/dev/null
python -m pip install -r $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT/src/requirements.txt &>/dev/null
deactivate

## add env var required by the wrapper
add_env_to_bashrc DOCTUM_HELPER_BIN_PATH_DEFAULT ${DOCTUM_HELPER_BIN_PATH_DEFAULT}

## fix exec rights for wrapper
# chmod +x $DOCTUM_HELPER_WRAPPER_PATH
chmod +x $HOME/$DOCTUM_HELPER_BIN_PATH_DEFAULT/venv/bin/activate

## try to create link to user bin folder (might fail for specifics linux distrib)
ln -s $DOCTUM_HELPER_WRAPPER_PATH /usr/$DOCTUM_HELPER_BIN_PATH_DEFAULT 2>/dev/null
if [ $? -ne 0 ];then
    ## other method to call script that has lesser chance to fail
    create_alias_in_bashrc $DOCTUM_HELPER_ALIAS_DEFAULT "bash $DOCTUM_HELPER_WRAPPER_PATH"
fi

## final message
echo "Doctum helper successfully installed, use 'dh' to launch it"
source $HOME/.bashrc
# echo "run 'source $HOME/.bashrc' in order to use alias '${DOCTUM_HELPER_ALIAS_DEFAULT}'"
