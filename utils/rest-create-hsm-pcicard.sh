#!/bin/bash

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file with hsm pci card definitions in it"
    exit
fi

token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  serial=$(echo $row | cut -f1 -d\,)
  fbno=$(echo $row | cut -f2 -d,)
  model=$(echo $row | cut -f3 -d,)
  manufacturedate=$(echo $row | cut -f4 -d,)
  compartment_id=$(echo $row | cut -f5 -d,)
  hsmdomain_id=$(echo $row | cut -f6 -d,)
  server_id=$(echo $row | cut -f7 -d,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

   http --verbose POST "${apiserverurl}/hsmpcicard/add" \
   "serial=${serial}" \
   "fbno=${fbno}" \
   "model=${model}" \
   "manufacturedate=${manufacturedate}" \
   "hsmdomain_id=${hsmdomain_id}" \
   "server_id=${server_id}" \
   "compartment_id=${compartment_id}" \
   "Authorization:Bearer $token"

done
