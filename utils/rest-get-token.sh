#!/bin/bash

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"


token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')
echo "${token}" > .token
