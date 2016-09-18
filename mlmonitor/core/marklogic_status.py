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
module responsible for retrieving MarkLogic statuses from Management REST API

docs for Management REST API calls - http://docs.marklogic.com/REST/management

NOTE - did not use marklogic-python api as that package is based on python 3.

"""

import logging
from http_utils import HTTPUtil

log = logging.getLogger(__name__)


class MarkLogicStatus:
    scheme = "http"

    def __init__(self, scheme=None, url=None, user=None, passwd=None, port=None, host=None, auth=None):
        self.url = url
        self.user = user
        self.passwd = passwd
        self.scheme = scheme
        self.port = port
        self.host = host
        self.auth = auth

    def get(self, resource=None, name=None, group=None):

        # compose GET URI to MarkLogic Management REST API
        path = "/manage/v2"
        if resource:
            path += "/" + resource
        if name:
            path += "/" + name
        path += "?view=status&format=json"
        if group:
            path += "&group-id=" + group

        # retrieve Management REST API status
        try:
            return HTTPUtil.http_get(scheme=self.scheme,
                                     host=self.host,
                                     port=self.port,
                                     path=path,
                                     user=self.user,
                                     passwd=self.passwd,
                                     realm="public",
                                     auth="DIGEST")
        except Exception as e:
            log.error("Problem accessing MarkLogic Management API")
            log.error(e)
            pass
