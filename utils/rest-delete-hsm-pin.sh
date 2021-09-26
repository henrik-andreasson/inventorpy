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
    echo "arg1 must be a file with hsm pin definitions in it"
    exit
fi


IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  keysn=$(echo $row | cut -f1 -d\,)
  user_name=$(echo $row | cut -f2 -d\,)
  compartment_name=$(echo $row | cut -f3 -d\,)
  hsmdomain_name=$(echo $row | cut -f4 -d\,)
  comment=$(echo $row | cut -f5 -d\,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

  result=$(http --verify cacerts.pem  "${API_URL}/hsmped" \
    keysn=${keysn} \
    hsmdomain_name=${hsmdomain_name} \
    "Authorization:Bearer $token")

  result_pedid=$(echo $result | jq '.id' | tr -d \")
  if [ "x${result_pedid}" == "x" ] ; then
    echo "failed to get ped ${keysn} + ${hsmdomain_name}"
    continue
  fi

   http --verify cacerts.pem --verbose DELETE "${API_URL}/hsmpin" \
   "ped_id=${result_pedid}" \
   "Authorization:Bearer $token"


done
