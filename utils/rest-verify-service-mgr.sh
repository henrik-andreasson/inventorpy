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
    echo "arg1 must be a file with service users definitions in it"
    echo "service,user"
    exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  service=$(echo $row | cut -f1 -d\,)
  mgr=$(echo $row | cut -f2 -d\,)

  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  result=$(http --verify cacerts.pem  "${API_URL}/service/manager/${service}" \
    "Authorization:Bearer $token")

  check_service_mgr=$(echo $result | jq '.manager' | tr -d '"' | grep "$mgr")

  if [ "x${check_service_mgr}" != "x" ] ; then
    echo "ok service mgr ${service}/${mgr}"
  else
    echo "fail service mgr wrong mgr of service: <${service}> user: <${mgr}>"
  fi

done
