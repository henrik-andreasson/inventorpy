#!/bin/bash

USE_CERT=0

if [ "x$CERT" != "x" ] ; then
  echo "$CERT" | tr ';' '\n' > /inventorpy/cert.pem
  let USE_CERT="$USE_CERT + 1"
fi

if [ "x$CA" != "x" ] ; then
  echo "$CA" | tr ';' '\n' > /inventorpy/ca.pem
  let USE_CERT="$USE_CERT + 1"
fi

if [ "x$KEY" != "x" ] ; then
  echo "$KEY" | tr ';' '\n' > /inventorpy/key.pem
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
         --pid /inventorpy/teamplan.pid \
         --keyfile /inventorpy/key.pem  \
         --certfile  /inventorpy/cert.pem ${EXTRA_OPTIONS}

else

    gunicorn inventorpy:app -b 0.0.0.0:${LISTEN} ${EXTRA_OPTIONS}

fi
