"""Testing utilities for MarkLogic Monitoring Plugin."""

from mlmonitor.cli.main import MLMonitorTestApp
from cement.utils.test import *

class MLMonitorTestCase(CementTestCase):
    app_class = MLMonitorTestApp

    def setUp(self):
        """Override setup actions (for every test)."""
        super(MLMonitorTestCase, self).setUp()

    def tearDown(self):
        """Override teardown actions (for every test)."""
        super(MLMonitorTestCase, self).tearDown()

