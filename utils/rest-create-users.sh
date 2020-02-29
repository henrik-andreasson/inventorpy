#!/bin/bash

# uses httpie  - pip3 install httpie

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file network definitions in it"
    echo "username,password,email,about_me"
    exit
fi

token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  username=$(echo $row | cut -f1 -d\,)
  password=$(echo $row | cut -f2 -d\,)
  email=$(echo $row | cut -f3 -d\,)
  about_me=$(echo $row | cut -f4 -d\,)

  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continiue
  fi
  http --verbose POST "${apiserverurl}/users" \
    "email=${email}" \
    "about_me=${about_me}" \
    "username=${username}" \
    "password=${password}" \
      "Authorization:Bearer $token"

done
