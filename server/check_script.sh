#!/bin/bash

#MIME_TYPE=$(file --mime-type -b $1)
MIME_TYPE=$(xdg-mime query filetype $1)

XATTR=$(getfattr --absolute-names -n security.selinux $1 |tail -n 2|head -n 1|tr '=' ' '|tr -d '"'|awk '{print $2}')
INTERPRETER_TYPE="system_u:object_r:interpreter_t"
WL_TYPE="system_u:object_r:whitelist_t"



function is_script()
{
    case $MIME_TYPE in
        application/x-shellscript) echo 1 ;;
	application/x-awk) echo 1 ;;
        application/x-csh) echo 1 ;;
	application/x-java) echo 1 ;;
	application/x-perl) echo 1 ;;
	application/x-php) echo 1 ;;
	application/x-ruby) echo 1 ;;
	application/x-sqlite3) echo 1 ;;
	application/javascript) echo 1 ;;
	text/x-cmake) echo 1 ;;
	text/x-csharp) echo 1 ;;
	#text/x-csrc) echo 1 ;;
	text/x-emacs-lisp) echo 1 ;;
	text/x-fortran) echo 1 ;;
	text/x-go) echo 1 ;;
	text/x-lua) echo 1 ;;
	text/x-makefile) echo 1 ;;
	text/x-matlab) echo 1 ;;
	text/x-python) echo 1 ;;
	text/x-python3) echo 1 ;;
	text/x-svsrc) echo 1 ;;
	text/x-systemd-unit) echo 1 ;;
	text/x-tcl) echo 1 ;;
	text/x-perl) echo 1 ;;
	text/x-java) echo 1 ;;
	text/x-haskell) echo 1 ;;
	text/x-pascal) echo 1 ;;
	text/x-scala) echo 1 ;;
	text/x-sh) echo 1 ;;
	text/x-install) echo 1 ;;
	text/x-shellscript) echo 1 ;;

        *) echo 0 ;;
    esac
}

function is_executable()
{
    case $MIME_TYPE in
        application/x-sharedlib) echo 1 ;;
	application/x-object) echo 1 ;;
	application/x-executable) echo 1 ;;
     	*) echo 0;;
    esac
}

IS_SCRIPT=$(is_script $MIME_TYPE)
IS_EXECUTABLE=$(is_executable $MIME_TYPE)

if [ $IS_SCRIPT == 1 ]; then
    echo This file: $1 is script file, MIME_TYPE=$MIME_TYPE

    # To Do for EVM sign here
    if [ "$XATTR" == "$WL_TYPE" ]; then
        sudo chcon -h -t interpreter_t $1
    fi
    sudo evmctl sign --imasig $1 -k /etc/keys/privkey_evm.pem

    exit
fi

if [ $IS_EXECUTABLE == 1 ]; then
    echo This file: $1 is executable file, MIME_TYPE=$MIME_TYPE

    # To Do for EVM sign here
    if [ "$XATTR" == "$WL_TYPE" ]; then
        sudo chcon -h -t whitelist_sign_t $1
    fi
    sudo evmctl sign --imasig $1 -k /etc/keys/privkey_evm.pem

    exit
fi


