#!/bin/bash

green_color='\e[0;32m'
red_color='\e[0;31m'
yellow_color='\e[0;33m'
rest_color='\e[0m'
mode=$1
tag_name=$2
port_number=$3

read -p "Do you want to delete databases folder?[Y/n] " delete_ans

if [[ $delete_ans == "Y" ]]; then
    echo -e "${yellow_color}The databases folder will be deleted.${rest_color}"
    if [[ $USER != 'root' ]]; then
        sudo_prefix="sudo "
    fi;
    if [[ $mode == "tls" ]]; then
        rm -rf ./tls_databases/
        mkdir ./tls_databases/
        ${sudo_prefix}chown -R "1000:1000" ./tls_databases/
        ${sudo_prefix}chmod -R 755 ./tls_databases/
    else
        rm -rf ./no_tls_databases/
        mkdir ./no_tls_databases/
        ${sudo_prefix}chown -R "1000:1000" ./no_tls_databases/
        ${sudo_prefix}chmod -R 755 ./no_tls_databases/
    fi;
else
    echo -e "${yellow_color}The databases folder will keep existed.${rest_color}"
fi;


if [[ $mode != "tls" && $mode != "no_tls" ]]; then
    echo -e "${red_color}The mode param should be tls or no_tls.${rest_color}"
    exit 1;
fi;

if [[ $tag_name == "" ]]; then
    echo -e "${yellow_color}The tag name is empty. It will use latest tag.${rest_color}"
    tag_name="latest"
fi;

if [[ $port_number == "" ]]; then
    echo -e "${yellow_color}IEC-61850 server will run on 8102...${rest_color}"
    port_number=8102
fi;

docker stop "$mode-iec61850-server" > /dev/null 2>&1
docker rm "$mode-iec61850-server" > /dev/null 2>&1

if [[ ! -f ./config_file ]]; then
    echo -e "${red_color}The ./config_file is not found${rest_color}"
    echo -e "${red_color}Please refer ./config.example file...${rest_color}"
    exit 1;
fi;

if [[ $mode == "tls" ]]; then
    docker run -d --name="$mode-iec61850-server" --restart=always -v $PWD/config_file:/home/iec61850/config --network host -v $PWD/tls_databases:/home/iec61850/databases -p "$port_number:$port_number" libiec61850:$tag_name -c "cd ./tls_server_example && ./tls_server_example $port_number"
fi;

if [[ $mode == "no_tls" ]]; then
    docker run -d --name="$mode-iec61850-server" --restart=always -v $PWD/config_file:/home/iec61850/config --network host -v $PWD/no_tls_databases:/home/iec61850/databases -p "$port_number:$port_number" libiec61850:$tag_name -c "cd ./no_tls_server_example && ./no_tls_server_example $port_number"
fi;

if [[ $? != 0 ]]; then
    echo -e "${red_color}IEC-61850 server container is failed to run...${rest_color}"
    exit 1;
fi;


echo -e "${green_color}IEC-61850 server run on $port_number successfully...${rest_color}"

