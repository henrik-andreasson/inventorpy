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
    echo "arg1 must be a file network definitions in it"
    echo "username,password,email,about_me"
    exit
fi



IFS=$'\n'

for row in $(cat "${csvfile}") ; do

  username=$(echo $row | cut -f1 -d\,)
  password=$(echo $row | cut -f2 -d\,)
  email=$(echo $row | cut -f3 -d\,)
  about_me=$(echo $row | cut -f4 -d\,)

  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continiue
  fi
  http --verify cacerts.pem --verbose POST "${apiserverurl}/users" \
    "email=${email}" \
    "about_me=${about_me}" \
    "username=${username}" \
    "password=${password}" \
      "Authorization:Bearer $token"

done
