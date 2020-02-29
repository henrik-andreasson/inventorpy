#!/bin/bash

# uses httpie  - pip3 install httpie

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file with location definitions in it"
    echo "name,safe_id,user_id"
    exit
fi

token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  name=$(echo $row | cut -f1 -d\,)
  safe_id=$(echo $row | cut -f2 -d\,)
  user_id=$(echo $row | cut -f3 -d\,)
  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  http --verbose POST "${apiserverurl}/compartment" \
    "name=${name}" \
    "safe_id=${safe_id}" \
    "user_id=${user_id}" \
    "Authorization:Bearer $token"

done