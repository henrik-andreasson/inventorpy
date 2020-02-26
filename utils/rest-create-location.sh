#!/bin/bash

# uses httpie  - pip3 install httpie

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file with location definitions in it"
    echo "Place (City/Region),Facillity (House),Area (Room/Rack/Safe),Position,Type of Facillity
"
    exit
fi

token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  place=$(echo $row | cut -f1 -d\,)
  facillity=$(echo $row | cut -f2 -d\,)
  area=$(echo $row | cut -f3 -d\,)
  position=$(echo $row | cut -f4 -d\,)
  type=$(echo $row | cut -f5 -d\,)
  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  http --verbose POST "${apiserverurl}/location" \
    "place=${place}" \
    "facillity=${facillity}" \
    "area=${area}" \
    "position=${position}" \
    "type=${type}" \
    "Authorization:Bearer $token"

done
