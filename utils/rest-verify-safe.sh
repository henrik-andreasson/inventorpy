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
    echo "arg1 must be a file with safe definitions in it"
    echo "name"
    exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do
  name=$(echo $row | cut -f1 -d\,)
  location_id=$(echo $row | cut -f2 -d\,)
  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

  # http --verbose --verify cacerts.pem  "${API_URL}/safe/${name}" \
  #   "Authorization:Bearer $token"

  result=$(http --verify cacerts.pem  "${API_URL}/safe/${name}" \
    "Authorization:Bearer $token")

# TODO: check more of the data set than just the name
  result_name=$(echo $result | jq '.name' | tr -d \")
  if [ "${name}" == "${result_name}" ] ; then
    echo "ok safe name ${name}"
  else
    echo "fail safe name <${name}> != <${result_name}>"
  fi
  result_loc=$(echo $result | jq '.location_id' | tr -d \")
  if [ "${location_id}" == "${result_loc}" ] ; then
    echo "ok safe location ${location_id}"
  else
    echo "fail safe location  <${location_id}> != <${result_loc}>"
  fi


done
