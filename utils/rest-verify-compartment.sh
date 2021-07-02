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
    echo "arg1 must be a file with server definitions in it"
    echo "name"
    exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  name=$(echo $row | cut -f1 -d\,)
  safe_name=$(echo $row | cut -f2 -d\,)
  username=$(echo $row | cut -f3 -d\,)

  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  result=$(http --verify cacerts.pem  "${API_URL}/compartment/by-name/${name}" \
    "Authorization:Bearer $token")

# TODO: check more of the data set in each server hd, cpu and so on
  result_name=$(echo $result | jq '.name' | tr -d \")
  if [ "${name}" == "${result_name}" ] ; then
    echo "ok compartment ${name}"
  else
    echo "fail compartment <${name}> != <${result_name}>"
  fi

  result_userid=$(echo $result | jq '.user_id' | tr -d \")
  user_result=$(http --verify cacerts.pem  "${API_URL}/users/${result_userid}" \
    "Authorization:Bearer $token")
  result_username=$(echo $user_result | jq '.username' | tr -d \")
  if [ "${username}" == "${result_username}" ] ; then
    echo "ok compartment username ${username}"
  else
    echo "fail compartment username <${username}> != <${result_username}>"
  fi


  result_safeid=$(echo $result | jq '.safe_id' | tr -d \")
  safe_result=$(http --verify cacerts.pem  "${API_URL}/safe/${result_safeid}" \
    "Authorization:Bearer $token")
  result_safe=$(echo $safe_result | jq '.name' | tr -d \")
  if [ "${safe_name}" == "${result_safe}" ] ; then
    echo "ok compartment safe ${safe_name}"
  else
    echo "fail compartment safe <${safe_name}> != <${result_safe}>"
  fi

done
