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

  ped_id=$(echo $row | cut -f1 -d\,)
  compartment_id=$(echo $row | cut -f2 -d,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

   http --verify cacerts.pem --verbose POST "${API_URL}/hsmpin/add" \
   "ped_id=${ped_id}" \
   "compartment_id=${compartment_id}" \
   "Authorization:Bearer $token"

done
