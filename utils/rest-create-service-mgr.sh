#!/bin/bash

if [ -f variables ] ; then
  . variables
  echo "URL: ${API_URL}"
  echo "User: ${API_USER}"

fi

if [ -f rest-get-token.sh ] ; then
  . rest-get-token.sh
  get_new_token
else
  echo "login/get token failed"
  exit
fi

if [ "x$1" != "x" ] ; then
    csvfile=$1
else
    echo "arg1 must be a file service users definitions in it"
    echo "service,username"
    exit
fi



IFS=$'\n'

for row in $(cat "${csvfile}") ; do

  service=$(echo $row | cut -f1 -d\,)
  username=$(echo $row | cut -f2 -d\,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  http --verify cacerts.pem --verbose POST "${API_URL}/service/manager/${service}" \
    "username=${username}" \
      "Authorization:Bearer $token"

done
