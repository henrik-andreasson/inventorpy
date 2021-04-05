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
  echo "arg1 must be a file with users definitions in it"
  echo "name"
  exit
fi


IFS=$'\n'

for row in $(cat "${csvfile}") ; do

  username=$(echo $row | cut -f1 -d\,)
  password=$(echo $row | cut -f2 -d\,)
  email=$(echo $row | cut -f3 -d\,)
  about_me=$(echo $row | cut -f4 -d\,)

  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  result=$(http --verify cacerts.pem  "${API_URL}/users/${username}" \
    "Authorization:Bearer $token")

  result_username=$(echo $result | jq '.username' | tr -d \")
  if [ "${username}" == "${result_username}" ] ; then
    echo "ok username ${username}"
  else
    echo "fail username <${username}> != <${result_username}>"
  fi

done
