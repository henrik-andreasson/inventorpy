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


result=$(http --verify cacerts.pem  "${API_URL}/compartmentlist" \
    "Authorization:Bearer $token" )

echo "# compartment_id,comp_name,safe_id,safe_id,user_id,username"

for row in $(echo ${result}| jq .[]) ; do

#  echo "$row"
  result=$(http --verify cacerts.pem   "${API_URL}/compartment/${row}" \
    "Authorization:Bearer $token" )

  result_userid=$(echo $result | jq '.user_id' | tr -d \")
  user_result=$(http --verify cacerts.pem  "${API_URL}/users/${result_userid}" \
    "Authorization:Bearer $token")
  result_username=$(echo $user_result | jq '.username' | tr -d \")

  result_safeid=$(echo $result | jq '.safe_id' | tr -d \")
  jsonsafe=$(http --verify cacerts.pem  "${API_URL}/safe/${result_safeid}" \
    "Authorization:Bearer $token")

  safe_name=$(echo $jsonsafe | jq '.name' | tr -d \")
  comp_name=$(echo "$result" | jq '.name'| tr -d \")
  echo "${row},${comp_name},${result_safeid},${safe_name},${result_userid},${result_username}"
done
