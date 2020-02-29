#!/bin/bash

# uses httpie  - pip3 install httpie

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file network definitions in it"
    echo "name,color"
    exit
fi

token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  name=$(echo $row | cut -f1 -d\,)
  color=$(echo $row | cut -f2 -d\,)

  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  http --verbose POST "${apiserverurl}/service" \
    "name=${name}" \
    "color=${color}" \
    "Authorization:Bearer $token"

done
