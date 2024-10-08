#!/bin/bash

if [ -f variables ] ; then
  . variables
  echo "# URL: ${API_URL}"
  echo "# User: ${API_USER}"

fi

token=""
if [ -f rest-get-token.sh ] ; then
  . rest-get-token.sh
  token=$(get_new_token 2>/dev/null)
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
    echo "name"
    exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  name=$(echo $row | cut -f1 -d\,)

  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

  result=$(http --verify cacerts.pem  "${API_URL}/server/${name}" \
    "Authorization:Bearer $token")

# TODO: check more of the data set in each server hd, cpu and so on
  result_name=$(echo $result | jq '.hostname' | tr -d \")
  if [ "${name}" == "${result_name}" ] ; then
    echo "ok server ${name}"
  else
    echo "fail server <${name}> != <${result_name}>"
  fi

done
