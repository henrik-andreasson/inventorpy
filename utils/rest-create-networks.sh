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
    echo "arg1 must be a file network definitions in it"
    echo "#netname,network,netmask,gateway,location,service"
    exit
fi

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
    continue
  fi
  http --verify cacerts.pem --verbose POST "${API_URL}/network/add" \
    "name=${name}" \
    "network=${network}" \
    "netmask=${netmask}" \
    "gateway=${gateway}" \
    "location_id=${location}" \
    "service_id=${service}" \
     "Authorization:Bearer $token"


done
