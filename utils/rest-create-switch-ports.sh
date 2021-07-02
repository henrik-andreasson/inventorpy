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
    echo "arg1 must be a file with location definitions in it"
    echo "name,location_id"
    exit
fi


IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  name=$(echo $row | cut -f1 -d\,)
  switch=$(echo $row | cut -f2 -d\,)
  server=$(echo $row | cut -f3 -d\,)
  server_if=$(echo $row | cut -f4 -d\,)
  network=$(echo $row | cut -f5 -d\,)
  comment=$(echo $row | cut -f6 -d\,)

  http --verify cacerts.pem --verbose POST "${API_URL}/switch/port/add" \
    "name=${name}" \
    "switch=${switch}" \
    "server_name=${server}" \
    "server_if=${server_if}" \
    "network_name=${network}" \
    "comment=${comment}" \
    "Authorization:Bearer $token"

done
