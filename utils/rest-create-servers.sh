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
  psu=$(echo $row | cut -f7 -d,)
  hd=$(echo $row | cut -f8 -d,)
  os_name=$(echo $row | cut -f9 -d,)
  os_version=$(echo $row | cut -f10 -d,)
  serial=$(echo $row | cut -f11 -d,)
  manufacturer=$(echo $row | cut -f12 -d,)
  model=$(echo $row | cut -f13 -d,)
  rack_name=$(echo $row | cut -f14 -d,)
  service_name=$(echo $row | cut -f15 -d,)
  status=$(echo $row | cut -f16 -d,)
  support_start=$(echo $row | cut -f17 -d,)
  support_end=$(echo $row | cut -f18 -d,)
  rack_position=$(echo $row | cut -f19 -d,)
  environment=$(echo $row | cut -f20 -d,)
  comment=$(echo $row | cut -f21 -d,)
  virtual_host=$(echo $row | cut -f22 -d,)


  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

   http --verify cacerts.pem --verbose POST "${API_URL}/server/add" \
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
    "virtual_host=${virtual_host}" \
     "Authorization:Bearer $token"

done
