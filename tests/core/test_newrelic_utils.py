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

# This is here to deal with a bug in in PyCharm 2016.3.  Can be removed/ignored as needed.
#from __future__ import absolute_import

import logging
import unittest

from mlmonitor.core.utils.newrelic_utils import NewRelicUtility

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

class NewRelicUtilsTests(unittest.TestCase):
    def testUpdate(self):
        response = NewRelicUtility.update_newrelic(self,
                                                   host="localhost",
                                                   pid=1234,
                                                   version="0.0.1",
                                                   name="marklogic_unittest",
                                                   guid="com.marklogic",
                                                   duration=60,
                                                   metrics={"Component/MarkLogic[UnitTest]": 100},
                                                   key="e8cf9b3d7aaca22a8632c7e01a14f8e722519b8a")
        log.debug(response)
        assert response
