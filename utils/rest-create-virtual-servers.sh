#!/bin/bash


if [ -f variables ] ; then
  . variables
  echo "URL: ${API_URL}"
  echo "User: ${API_USER}"

fi

token=""
if [ -f rest-get-token.sh ] ; then
  . rest-get-token.sh
  token=$(get_new_token)
  if [ $? -ne 0 ] ; then
    echo "failed to get a login token"
    exit
  fi
else
  echo "login/get token failed"
  exit
fi

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file with server definitions in it"
    exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  hostname=$(echo $row | cut -f1 -d\,)
  role=$(echo $row | cut -f2 -d\,)
  ipaddress=$(echo $row | cut -f3 -d\,)
  network=$(echo $row | cut -f4 -d,)
  memory=$(echo $row | cut -f5 -d,)
  cpu=$(echo $row | cut -f6 -d,)
  hd=$(echo $row | cut -f7 -d,)
  os_name=$(echo $row | cut -f8 -d,)
  os_version=$(echo $row | cut -f9 -d,)
  service_name=$(echo $row | cut -f10 -d,)
  status=$(echo $row | cut -f11 -d,)
  environment=$(echo $row | cut -f12 -d,)
  comment=$(echo $row | cut -f13 -d,)
  hosting_server_name=$(echo $row | cut -f14 r-d,)


  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

   http --verify cacerts.pem --verbose POST "${API_URL}/virtual_server/add" \
    "hostname=${hostname}" \
    "role=${role}" \
    "ipaddress=${ipaddress}" \
    "network_name=${network}" \
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
    "rack_name=${rack_name}" \
    "service_name=${service_name}" \
    "support_start=${support_start}" \
    "support_end=${support_end}" \
    "environment=${environment}" \
    "comment=${comment}" \
    "rack_position=${rack_position}" \
    "hosting_server_name=${hosting_server_name}" \
     "Authorization:Bearer $token"

done
