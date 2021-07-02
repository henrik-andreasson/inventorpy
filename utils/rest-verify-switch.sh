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
    echo "arg1 must be a file network definitions in it"
    echo "name"
    exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

    name=$(echo $row | cut -f1 -d\,)
    alias=$(echo $row | cut -f2 -d\,)
    ipaddress=$(echo $row | cut -f3 -d\,)
    serial=$(echo $row | cut -f4 -d\,)
    manufacturer=$(echo $row | cut -f5 -d\,)
    model=$(echo $row | cut -f6 -d\,)
    rack=$(echo $row | cut -f7 -d\,)
    rack_position=$(echo $row | cut -f8 -d\,)
    service=$(echo $row | cut -f9 -d\,)
    status=$(echo $row | cut -f10 -d\,)
    support_start=$(echo $row | cut -f11 -d\,)
    support_end=$(echo $row | cut -f12 -d\,)
    comment=$(echo $row | cut -f13 -d\,)
    iscomment=$(echo $row | grep "^#" )
    if [ "x$iscomment" != "x" ] ; then
      continue
    fi


  result=$(http --verify cacerts.pem  "${API_URL}/switch/${name}" \
    "Authorization:Bearer $token")

  result_name=$(echo $result | jq '.name' | tr -d \")
  if [ "${name}" == "${result_name}" ] ; then
    echo "ok switch ${name}"
  else
    echo "fail switch <${name}> != <${result_name}>"
  fi

#TODO: all check all attributes ...

done
