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
    echo "arg1 must be a file with rack definitions in it"
    echo "name"
    exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  name=$(echo $row | cut -f1 -d\,)
  location_long_name=$(echo $row | cut -f2 -d\,)
  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
#  http --verify cacerts.pem  "${API_URL}/rack/${name}" \
#    "Authorization:Bearer $token"
  result=$(http --verify cacerts.pem  "${API_URL}/rack/${name}" \
    "Authorization:Bearer $token")

  result_name=$(echo $result | jq '.name' | tr -d \")
  if [ "${name}" == "${result_name}" ] ; then
    echo "ok rack ${name}"
  else
    echo "fail rack <${name}> != <${result_name}>"
  fi

  result_location_id=$(echo $result | jq '.location_id' | tr -d \")

#  http --verify cacerts.pem  "${API_URL}/location/${result_location_id}" \
#    "Authorization:Bearer $token"
  result_location_json=$(http --verify cacerts.pem  "${API_URL}/location/${result_location_id}" \
    "Authorization:Bearer $token")
 result_loc_long="$(echo $result_location_json | jq .place | tr -d '"') / $(echo $result_location_json | jq .facillity | tr -d '"') / $(echo $result_location_json | jq .area | tr -d '"') / $(echo $result_location_json | jq .position | tr -d '"')"
  if [ "${location_long_name}" == "${result_loc_long}" ] ; then
    echo "ok rack location_long_name ${location_long_name}"
  else
    echo "fail rack location_long_name <${location_long_name}> != <${result_loc_long}>"
  fi

done
