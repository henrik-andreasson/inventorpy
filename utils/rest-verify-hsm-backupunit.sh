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
    echo "arg1 must be a file with hsm backup units definitions in it"
    exit
fi


IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  name=$(echo $row | cut -f1 -d\,)
  serial=$(echo $row | cut -f2 -d\,)
  fbno=$(echo $row | cut -f3 -d\,)
  model=$(echo $row | cut -f4 -d\,)
  manufacturedate=$(echo $row | cut -f5 -d\,)
  safe_name=$(echo $row | cut -f6 -d\,)
  hsmdomain_name=$(echo $row | cut -f7 -d\,)
  comment=$(echo $row | cut -f8 -d\,)
  iscomment=$(echo $row | grep "#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi

#  http --verify cacerts.pem   "${API_URL}/hsm_backup_unit/${name}" \
#  "Authorization:Bearer $token"

   result=$(http --verify cacerts.pem   "${API_URL}/hsm_backup_unit/${name}" \
   "Authorization:Bearer $token")

   result_fbno=$(echo $result | jq '.fbno' | tr -d \")
   if [ "${fbno}" == "${result_fbno}" ] ; then
       echo "ok hsm-backup-unit fbno ${fbno}"
   else
       echo "fail hsm-backup-unit fbno <${fbno}> != <${result_fbno}>"
   fi

   result_model=$(echo $result | jq '.model' | tr -d \")
   if [ "${model}" == "${result_model}" ] ; then
       echo "ok hsm-backup-unit model ${model}"
   else
       echo "fail hsm-backup-unit model <${model}> != <${result_model}>"
   fi

done
