#!/bin/bash

# uses httpie  - pip3 install httpie

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file network definitions in it"
    echo "#netname,network,netmask,gateway,location,service"
    exit
fi

token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')


for row in $(cat "${csvfile}") ; do

#netname,network,netmask,gateway,location,service
# CS-PROD-CA-G1,164.9.136.0,255.255.255.240,164.9.136.1,5,2

  name=$(echo $row | cut -f1 -d\,)
  network=$(echo $row | cut -f2 -d\,)
  netmask=$(echo $row | cut -f3 -d,)
  gateway=$(echo $row | cut -f4 -d,)
  location=$(echo $row | cut -f5 -d,)
  service=$(echo $row | cut -f6 -d,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continiue
  fi
  http --verbose POST "${apiserverurl}/network/add" \
    "name=${name}" \
    "network=${network}" \
    "netmask=${netmask}" \
    "gateway=${gateway}" \
    "location_id=${location}" \
    "service_id=${service}" \
     "Authorization:Bearer $token"


done
