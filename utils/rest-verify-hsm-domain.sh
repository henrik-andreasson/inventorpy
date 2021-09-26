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
    echo "arg1 must be a file with hsm-domain definitions in it"
    echo "name,service"
    exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do
  name=$(echo $row | cut -f1 -d\,)
  service_name=$(echo $row | cut -f2 -d\,)
  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

  result=$(http --verify cacerts.pem  "${API_URL}/hsmdomain/${name}" \
    "Authorization:Bearer $token")

  result_name=$(echo $result | jq '.name' | tr -d \")
  if [ "${name}" == "${result_name}" ] ; then
    echo "ok hsm-domain name ${name}"
  else
    echo "fail hsm-domain name <${name}> != <${result_name}>"
  fi
  result_service_id=$(echo $result | jq '.service_id' | tr -d \")
  if [ "x${result_service_id}" != "x" ] ;then
    service_result=$(http --verify cacerts.pem  "${API_URL}/service/${result_service_id}" \
      "Authorization:Bearer $token")

      service_name_result=$(echo $service_result | jq '.name' | tr -d \")
      if [ "${service_name}" == "${service_name_result}" ] ; then
        echo "ok hsm-domain service ${service_name}"
      else
        echo "fail hsm-domain service <${service_name}> != <${service_name_result}>"
      fi

    fi

done
