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
    echo "name,safe_id,user_id"
    exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

#compartment_id,comp_name,safe_id,safe_id,user_id,username
  id=$(echo $row | cut -f1 -d\,)
  name=$(echo $row | cut -f2 -d\,)
  safe_id=$(echo $row | cut -f3 -d\,)
  safe_name=$(echo $row | cut -f4 -d\,)
  user_id=$(echo $row | cut -f5 -d\,)
  username=$(echo $row | cut -f6 -d\,)
  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  http --verify cacerts.pem --verbose POST "${API_URL}/compartment/${id}" \
    "name=${name}" \
    "safe_name=${safe_name}" \
    "username=${username}" \
    "Authorization:Bearer $token"

done