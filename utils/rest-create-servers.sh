#!/bin/bash

read -p "username > " user_name
read -p "password > " pass_word
apiserverurl="http://127.0.0.1:5000/api"

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file with server definitions in it"
    exit
fi

token=$(http --auth "$user_name:$pass_word" POST "${apiserverurl}/tokens" | jq ".token" | sed 's/\"//g')

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  hostname=$(echo $row | cut -f1 -d\,)
  ipaddress=$(echo $row | cut -f2 -d\,)
  netmask=$(echo $row | cut -f3 -d,)
  gateway=$(echo $row | cut -f4 -d,)
  memory=$(echo $row | cut -f5 -d,)
  cpu=$(echo $row | cut -f6 -d,)
  psu=$(echo $row | cut -f7 -d,)
  hd=$(echo $row | cut -f8 -d,)
  os_name=$(echo $row | cut -f9 -d,)
  os_version=$(echo $row | cut -f10 -d,)
  serial=$(echo $row | cut -f11 -d,)
  manufacturer=$(echo $row | cut -f12 -d,)
  model=$(echo $row | cut -f13 -d,)
  rack_id=$(echo $row | cut -f14 -d,)
  location_id=$(echo $row | cut -f15 -d,)
  service_id=$(echo $row | cut -f16 -d,)
  status=$(echo $row | cut -f17 -d,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

   http --verbose POST "${apiserverurl}/server/add" \
    "hostname=${hostname}" \
    "ipaddress=${ipaddress}" \
    "netmask=${netmask}" \
    "gateway=${gateway}" \
    "memory=${memory}" \
    "cpu=${cpu}" \
    "psu=${psu}" \
    "hd=${hd}" \
    "os_name=${os_name}" \
    "os_version=${os_version}" \
    "serial=${serial}" \
    "manufacturer=${manufacturer}" \
    "model=${model}" \
    "status=${status}" \
    "rack_id=${rack_id}" \
    "location_id=${location_id}" \
    "service_id=${service_id}" \
     "Authorization:Bearer $token"

done
