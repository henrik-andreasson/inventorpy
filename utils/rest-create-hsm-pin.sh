#!/bin/bash

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file with hsm pin definitions in it"
    exit
fi

token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  ped_id=$(echo $row | cut -f1 -d\,)
  compartment_id=$(echo $row | cut -f2 -d,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

   http --verbose POST "${apiserverurl}/hsmpin/add" \
   "ped_id=${ped_id}" \
   "compartment_id=${compartment_id}" \
   "Authorization:Bearer $token"

done
