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
    echo "arg1 must be a file with hsm pci card definitions in it"
    exit
fi


IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  serial=$(echo $row | cut -f1 -d\,)
  fbno=$(echo $row | cut -f2 -d,)
  model=$(echo $row | cut -f3 -d,)
  manufacturedate=$(echo $row | cut -f4 -d,)
  safe_name=$(echo $row | cut -f5 -d,)
  hsmdomain_name=$(echo $row | cut -f6 -d,)
  server_name=$(echo $row | cut -f7 -d,)
  name=$(echo $row | cut -f8 -d,)
  contract=$(echo $row | cut -f9 -d\,)
  support_start=$(echo $row | cut -f10 -d\,)
  support_end=$(echo $row | cut -f11 -d\,)
  status=$(echo $row | cut -f12 -d\,)
  comment=$(echo $row | cut -f13 -d\,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

   http --verify cacerts.pem --verbose POST "${API_URL}/hsmpcicard/add" \
   "serial=${serial}" \
   "fbno=${fbno}" \
   "model=${model}" \
   "manufacturedate=${manufacturedate}" \
   "hsmdomain_name=${hsmdomain_name}" \
   "server_name=${server_name}" \
   "safe_name=${safe_name}" \
   "name=${name}" \
   "contract=${contract}" \
   "support_start=${support_start}" \
   "support_end=${support_end}" \
   "status=${status}" \
   "comment=${comment}" \
   "Authorization:Bearer $token"

done
