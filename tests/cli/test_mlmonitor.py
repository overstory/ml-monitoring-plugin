"""CLI tests for mlmonitor."""

from mlmonitor.utils import test

class CliTestCase(test.MLMonitorTestCase):
    def test_mlmonitor_cli(self):
        argv = ['--foo=bar']
        with self.make_app(argv=argv) as app:
            app.run()
            self.eq(app.pargs.foo, 'bar')
