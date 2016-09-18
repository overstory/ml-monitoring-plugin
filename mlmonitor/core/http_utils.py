#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016 MarkLogic Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0#
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""
http utils dependent on requests module (https://github.com/kennethreitz/requests)

"""

import logging
import requests
import sys
from requests.auth import HTTPDigestAuth, HTTPBasicAuth

log = logging.getLogger(__name__)


class HTTPUtil:

    def __init__(self):
        pass

    @staticmethod
    def http_get(scheme=None, host=None, port=None, path=None, user=None, passwd=None, realm=None, auth=None, url=None,
                 headers={'Accept': 'application/json'}, format="json", proxy=None):
        log.debug("dereference http GET")
        try:
            if url:
                requrl = url
            else:
                requrl = scheme + "://" + host + ":"
                requrl += repr(port)
                requrl += path
                log.debug(requrl)

            if auth == "DIGEST":
                auth = HTTPDigestAuth(user, passwd)
            elif auth == "BASIC":
                auth = HTTPBasicAuth(user, passwd)
            else:
                auth = None
            response = requests.get(requrl, auth=auth, headers=headers)

            if response.status_code == 200:
                if format == "json":
                    return response.json()
                else:
                    log.error("Must dereference json representation.")
                    # return a response to aid testing http GET
                    return response
            else:
                log.error("HTTP Request returned " + str(response.status_code) + " when accessing "+ requrl + " , check configuration.")
                sys.exit(1)
            return

        except requests.exceptions.Timeout:
            log.error("timeout error")
        except requests.exceptions.TooManyRedirects:
            log.error("too many redirects")
        except requests.exceptions.RequestException as e:
            log.error(e)
            sys.exit(1)
        return

    @staticmethod
    def http_post(scheme=None, host=None, port=None, path=None, user=None, passwd=None, realm=None, auth=None, url=None,
                  headers={'Accept': 'application/json'}, format="json", payload=None, proxy=None):
        log.debug("execute http post call")
        try:
            if url:
                requrl = url
            else:
                requrl = scheme + "://" + host + ":"
                requrl += repr(port)
                requrl += path
                log.debug(requrl)

            if auth == "DIGEST":
                auth = HTTPDigestAuth(user, passwd)
            elif auth == "BASIC":
                auth = HTTPBasicAuth(user, passwd)
            else:
                auth = None
            response = requests.post(requrl, json=payload, auth=auth, headers=headers, proxies=proxy)
            if format == "json":
                return response.json()
            else:
                return response.headers

        except requests.exceptions.Timeout:
            log.error("timeout error")
        except requests.exceptions.TooManyRedirects:
            log.error("too many redirects")
        except requests.exceptions.RequestException as e:
            log.error(e)
            sys.exit(1)
        return
