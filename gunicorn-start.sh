#!/bin/bash

if [ "x${INSTALL_PATH}" == "x" ] ; then

	if [ -d "/inventorpy" ] ; then
		INSTALL_PATH=/inventorpy
	elif [ -d "/opt/inventorpy" ] ; then
		INSTALL_PATH=/opt/inventorpy
	fi
fi

cd "${INSTALL_PATH}"

USE_CERT=0

if [ "x$CERT" != "x" ] ; then
  echo "$CERT" | tr ';' '\n' > "${INSTALL_PATH}/cert.pem"
  let USE_CERT="$USE_CERT + 1"
fi

if [ "x$CA" != "x" ] ; then
  echo "$CA" | tr ';' '\n' > "${INSTALL_PATH}/ca.pem"
  let USE_CERT="$USE_CERT + 1"
fi

if [ "x$KEY" != "x" ] ; then
  echo "$KEY" | tr ';' '\n' > "${INSTALL_PATH}/key.pem"
  let USE_CERT="$USE_CERT + 1"
fi

if [ "x${PORT}" != "x" ] ; then
  LISTEN="${PORT}"
else
  LISTEN=8080
fi

EXTRA_OPTIONS=""
if [ "x$OPTIONS" != "x" ] ; then
  EXTRA_OPTIONS="$OPTIONS"
else
  EXTRA_OPTIONS=""
fi



if [ $USE_CERT -gt 1 ] ; then

    gunicorn inventorpy:app -b 0.0.0.0:${LISTEN} \
         --pid "${INSTALL_PATH}/teamplan.pid" \
         --keyfile "${INSTALL_PATH}/key.pem"  \
         --certfile  "${INSTALL_PATH}/cert.pem" ${EXTRA_OPTIONS}

else

    gunicorn inventorpy:app -b 0.0.0.0:${LISTEN} ${EXTRA_OPTIONS}

fi
