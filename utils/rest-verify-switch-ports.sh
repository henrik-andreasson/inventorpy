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
  switch=$(echo $row | cut -f2 -d\,)
  server=$(echo $row | cut -f3 -d\,)
  server_if=$(echo $row | cut -f4 -d\,)
  network=$(echo $row | cut -f5 -d\,)
  comment=$(echo $row | cut -f6 -d\,)

  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
      continue
  fi

  result=$(http --verify cacerts.pem  POST "${API_URL}/switch/port/by-name/${switch}" name=${name} \
    "Authorization:Bearer $token" )

  result_name=$(echo $result | jq '.name' | tr -d \")
  if [ "${name}" == "${result_name}" ] ; then
    echo "ok switch port ${name}"
  else
    echo "fail switch port <${name}> != <${result_name}>"
  fi

  sw_result=$(http --verify cacerts.pem  "${API_URL}/switch/${switch}" \
    "Authorization:Bearer $token" )

  switch_id=$(echo $sw_result | jq '.id' | tr -d \")

  result_switch=$(echo $result | jq '.switch_id' | tr -d \")
  if [ "${switch_id}" == "${result_switch}" ] ; then
    echo "ok switch ${switch}/${switch_id}"
  else
    echo "fail switch <${switch_id}> != <${result_switch}>"
  fi

#TODO: all check all attributes ...

done
