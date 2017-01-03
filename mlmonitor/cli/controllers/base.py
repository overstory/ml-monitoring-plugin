"""MarkLogic Monitoring Plugin base controller."""

from cement.ext.ext_argparse import ArgparseController, expose
from mlmonitor.core import RunPlugin

class MLMonitorBaseController(ArgparseController):
    class Meta:
        label = 'base'
        description = 'Universal monitoring plugin for MarkLogic'
        # arguments = [
        #     (['-f', '--foo'],
        #      dict(help='the notorious foo option', dest='foo', action='store',
        #           metavar='TEXT') ),
        #     ]

    @expose(help="Starts up process to monitor MarkLogic with New Relic")
    def newrelic(self):
        self.app.log.info("Inside base.newrelic function.")
        self.app.log.debug("Inside base.newrelic function debug.")
        plugin = RunPlugin(config=self.app.config)
        plugin.run()
