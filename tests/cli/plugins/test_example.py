"""Tests for Example Plugin."""

from mlmonitor.utils import test

class ExamplePluginTestCase(test.MLMonitorTestCase):
    def test_load_example_plugin(self):
        self.app.setup()
        self.app.plugin.load_plugin('example')
