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
  echo "arg1 must be a file with location definitions in it"
  echo "Place (City/Region),Facillity (House),Area (Room/Rack/Safe),Position,Type of Facillity"
  exit
fi

IFS=$'\n'
for row in $(cat "${csvfile}") ; do

  place=$(echo $row | cut -f1 -d\,)
  facillity=$(echo $row | cut -f2 -d\,)
  area=$(echo $row | cut -f3 -d\,)
  position=$(echo $row | cut -f4 -d\,)
  type=$(echo $row | cut -f5 -d\,)
  iscomment=$(echo $row | grep "^#" )
  if [ "x$iscomment" != "x" ] ; then
    continue
  fi
  result=$(http  --verify cacerts.pem POST "${API_URL}/location/get" \
    "place=${place}" \
    "facillity=${facillity}" \
    "area=${area}" \
    "position=${position}" \
    "type=${type}" \
    "Authorization:Bearer $token")

  result_place=$(echo $result | jq '.place' | tr -d \")
  result_facillity=$(echo $result | jq '.facillity' | tr -d \")
  result_area=$(echo $result | jq '.area' | tr -d \")
  result_position=$(echo $result | jq '.type' | tr -d \")
  result_type=$(echo $result | jq '.type' | tr -d \")

  if [ "${place}" == "${result_place}" ] ; then
    echo "ok place ${place}"
  else
    echo "fail place <${place}> != <${result_place}>"
  fi

  if [ "${facillity}" == "${result_facillity}" ] ; then
    echo "ok facillity ${facillity}"
  else
    echo "fail facillity <${facillity}> != <${result_facillity}>"
  fi

  if [ "${area}" == "${result_area}" ] ; then
    echo "ok area ${area}"
  else
    echo "fail area <${area}> != <${result_area}>"
  fi

  if [ "${type}" == "${result_type}" ] ; then
    echo "ok type ${type}"
  else
    echo "fail type <${type}> != <${result_type}>"
  fi

done
