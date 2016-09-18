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

import logging
import sys
import unittest
from StringIO import StringIO

import newrelic_marklogic_plugin

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class PluginTests(unittest.TestCase):
    def testVersion(self):
        assert newrelic_marklogic_plugin.__version__ == "0.2.2"

    def testRunPlugin(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        nrml = newrelic_marklogic_plugin.RunPlugin(logFile='newrelic_marklogic_plugin.log',
                                                   confFile='etc/newrelic_marklogic.conf.sample')
        nrml.statusUpdate()
        self.assertEqual(sys.stdout.getvalue().strip(),'')

    def testConfigFile(self):
        nrml = newrelic_marklogic_plugin.RunPlugin(logFile='newrelic_marklogic_plugin.log',
                                                   confFile='etc/newrelic_marklogic.conf.sample')
        nrml.statusUpdate()
        self.assertEqual(nrml.ml_user, "admin")
        self.assertEqual(nrml.ml_pass, "admin")

    def testUsageMessage(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        nrml = newrelic_marklogic_plugin.RunPlugin(logFile='newrelic_marklogic_plugin.log',
                                                   confFile='etc/newrelic_marklogic.conf.sample')
        nrml.usage()
        self.assertEqual(sys.stdout.getvalue().strip(),
                         'newrelic_marklogic v' + newrelic_marklogic_plugin.__version__ + ' - NewRelic plugin for monitoring MarkLogic.\n\nusage: ./newrelic_marklogic.py [-h] [-c config file] [-l log file]\n\n    -h print usage instructions  (this message)\n    -c config file               (default: newrelic_marklogic.conf)\n    -l log file                  (default: newrelic_marklogic.log)')
