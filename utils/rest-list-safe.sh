#!/bin/bash

# uses httpie  - pip3 install httpie

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"


token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')

http --verbose "${apiserverurl}/safelist"  "Authorization:Bearer $token"
