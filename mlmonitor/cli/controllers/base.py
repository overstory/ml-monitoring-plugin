"""MarkLogic Monitoring Plugin base controller."""

from cement.ext.ext_argparse import ArgparseController, expose

from core.utils.statsd_utils import StatsdUtility
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

    @expose(help="Starts up process to send status update from MarkLogic to New Relic")
    def newrelic(self):
        plugin = RunPlugin(config=self.app.config)
        plugin.run()

    @expose(help="Starts up process to send status update from MarkLogic to StatsD")
    def statsd(self):
        stat_sets = create_stat_sets(self.app.config)
        for stat_set in stat_sets.items():
            stat_set.calculate()
            for stat in stat_set.stats.items():
                StatsdUtility.update_statsd(stat.statsd())




