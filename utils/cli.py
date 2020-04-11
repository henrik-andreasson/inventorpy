#!/usr/bin/python3

import requests
import argparse
import datetime
import hashlib
import json
import os
import syslog

DEFAULT_USER = "admin"
DEFAULT_PASS = "foo123"
SERVER_API_HOST = "http://localhost:5000"
SERVER_API_PATH = "api"
DEBUG = 0
SEND_LOG = 0


def get_token():

    url = "{}/{}/{}".format(SERVER_API_HOST, SERVER_API_PATH, "tokens")
    session = requests.Session()
    session.auth = (DEFAULT_USER, DEFAULT_PASS)

    auth = session.post(url)
#    r = requests.post(url,)
#    print("%s;%s" % (auth.status_code, auth.text))
    if auth.status_code == 200:
        serverinfo = json.loads(auth.text)
        token = serverinfo['token']
#        print("token: %s" % token)
        return token
    else:
        #        print(auth.status_code, auth.text)
        return


def id2value(module, id, key):

    #    print("%s <> %s <> %s" % (module, id, key))
    url = "{}/{}/{}/{}".format(SERVER_API_HOST, SERVER_API_PATH, module, id)
#    print("url: %s" % url)
    r = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)})

#    print("%s;%s" % (r.status_code, r.text))

    if r.status_code == 200:
        serverinfo = json.loads(r.text)
        value = serverinfo[key]
#        print("value: %s" % value)
        return value
    else:
        print(r.status_code, r.text)
        return


def add_item(module, string):

    url = "{}/{}/{}".format(SERVER_API_HOST, SERVER_API_PATH, module)

    r = requests.post(url, json=string, headers={'Authorization': 'Bearer {}'.format(token)})

    #    r = requests.post(url, cert=(opts.clientcert, opts.clientkey),
    #                      verify=opts.cacert, files=files, data=data)

    print("%s;%s" % (r.status_code, r.text))


def get_item(module, string):

    url = "{}/{}/{}/{}".format(SERVER_API_HOST, SERVER_API_PATH, module, string)
    print("posting to %s with string %s" % (module, string))
    r = requests.get(url, json=string, headers={'Authorization': 'Bearer {}'.format(token)})

    #    r = requests.post(url, cert=(opts.clientcert, opts.clientkey),
    #                      verify=opts.cacert, files=files, data=data)

    print("%s;%s" % (r.status_code, r.text))


def list_item(module):

    url = "{}/{}/{}list".format(SERVER_API_HOST, SERVER_API_PATH, module)
    print("posting to %s" % (url))
    r = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)})

    #    r = requests.post(url, cert=(opts.clientcert, opts.clientkey),
    #                      verify=opts.cacert, files=files, data=data)

    print("%s;%s" % (r.status_code, r.text))


parser = argparse.ArgumentParser()
parser.add_argument("--add", help="add to inventory")
parser.add_argument("--get", help="get from inventory")
parser.add_argument("--list", help="list in inventory")
parser.add_argument("--id", help="id argument")
parser.add_argument("--value", help="value argument")

args = parser.parse_args()

token = get_token()

if args.add:
    if args.value is None:
        print("--value must be used")
    else:
        add_item(args.add, args.value)
elif args.get:
    if args.id is None:
        print("--id must be used")
    else:
        if args.value:
            value = id2value(args.get, args.id, args.value)
            print(value)
        else:
            get_item(args.get, args.id)
elif args.list:
    list_item(args.list)
else:
    print("no such mode")
