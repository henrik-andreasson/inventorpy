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

page=""
if [ "x$1" != "x" ] ; then
  page="page=$1"
fi

http --verify cacerts.pem --verbose GET "${API_URL}/hsmpin/list?$page" \
   "Authorization:Bearer $token"
