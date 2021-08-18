#!/bin/bash

sudo chcon -t whitelist_t $1
sudo /usr/bin/check_script.sh $1
