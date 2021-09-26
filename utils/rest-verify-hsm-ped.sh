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
    echo "arg1 must be a file with hsm pci card definitions in it"
    exit
fi


IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  keyno=$(echo $row | cut -f1 -d\,)
  keysn=$(echo $row | cut -f2 -d\,)
  user_name=$(echo $row | cut -f3 -d\,)
  compartment_name=$(echo $row | cut -f4 -d\,)
  type=$(echo $row | cut -f5 -d\,)
  hsmdomain_name=$(echo $row | cut -f6 -d\,)
  comment=$(echo $row | cut -f7 -d\,)
  duplicate_of=$(echo $row | cut -f8 -d\,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

  result=$(http --verify cacerts.pem  "${API_URL}/hsmped/" \
    keysn=${keysn} \
    hsmdomain_name=${hsmdomain_name} \
    "Authorization:Bearer $token")

#  echo  "$result"
  result_keysn=$(echo $result | jq '.keysn' | tr -d \")
  if [ "${keysn}" == "${result_keysn}" ] ; then
    echo "ok hsm-ped sn ${keysn}"
  else
    echo "fail hsm-ped sn <${keysn}> != <${result_keysn}>"
  fi

  result_type=$(echo $result | jq '.type' | tr -d \")
  if [ "x${type}" == "x${result_type}" ] ; then
      echo "ok hsm-ped type ${type}"
  else
      echo "fail hsm-ped <${type}> != <${result_type}>"
  fi

done
