#!/bin/bash

apiserverurl="http://127.0.0.1:5000/api"

token=$(cat .token)

http --verbose "${apiserverurl}/${1}/${2}"  "Authorization:Bearer $token"
