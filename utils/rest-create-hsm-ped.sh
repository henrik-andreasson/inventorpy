#!/bin/bash

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file with hsm ped definitions in it"
    exit
fi

token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  keyno=$(echo $row | cut -f1 -d\,)
  keysn=$(echo $row | cut -f2 -d,)
  hsmdomain_id=$(echo $row | cut -f3 -d,)
  user_id=$(echo $row | cut -f4 -d,)
  compartment_id=$(echo $row | cut -f5 -d,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

   http --verbose POST "${apiserverurl}/hsmped/add" \
   "keyno=${keyno}" \
   "keysn=${keysn}" \
   "hsmdomain_id=${hsmdomain_id}" \
   "user_id=${user_id}" \
   "compartment_id=${compartment_id}" \
   "Authorization:Bearer $token"

done
