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

  serial=$(echo $row | cut -f1 -d\,)
  fbno=$(echo $row | cut -f2 -d\,)
  model=$(echo $row | cut -f3 -d\,)
  manufacturedate=$(echo $row | cut -f4 -d\,)
  safe_name=$(echo $row | cut -f5 -d\,)
  hsmdomain_name=$(echo $row | cut -f6 -d\,)
  server_name=$(echo $row | cut -f7 -d\,)
  name=$(echo $row | cut -f8 -d\,)
  contract=$(echo $row | cut -f9 -d\,)
  support_start=$(echo $row | cut -f10 -d\,)
  support_end=$(echo $row | cut -f11 -d\,)
  status=$(echo $row | cut -f12 -d\,)
  comment=$(echo $row | cut -f13 -d\,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  result=$(http --verify cacerts.pem  "${API_URL}/hsmpcicard/${name}" \
    "Authorization:Bearer $token")

  echo  "$result"
  result_name=$(echo $result | jq '.name' | tr -d \")
  if [ "${name}" == "${result_name}" ] ; then
    echo "ok hsm-pci-card name ${name}"
  else
    echo "fail hsm-pci-card name <${name}> != <${result_name}>"
  fi

  result_serial=$(echo $result | jq '.serial' | tr -d \")
  if [ "x${result_serial}" == "x${serial}" ] ; then
      echo "ok hsm-pci-card serial ${serial}"
  else
      echo "fail hsm-pci-card serial <${serial}> != <${result_serial}>"
  fi

  result_fbno=$(echo $result | jq '.fbno' | tr -d \")
  if [ "x${result_fbno}" == "x${fbno}" ] ; then
      echo "ok hsm-pci-card fbno ${fbno}"
  else
      echo "fail hsm-pci-card fbno <${fbno}> != <${result_fbno}>"
  fi

done
