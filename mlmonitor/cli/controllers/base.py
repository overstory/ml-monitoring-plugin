"""MarkLogic Monitoring Plugin base controller."""
from importlib import import_module

import time
import yaml
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
        while True:
            try:
                stat_sets = self.create_stat_sets()
                for stat_set in stat_sets:
                    stat_set.calculate()
                    for stat in stat_set.stats:
                        StatsdUtility.update_statsd(stat.statsd(),
                                                    host=self.app.config.get('statsd', 'host'),
                                                    port=int(self.app.config.get('statsd', 'port')))
            except Exception as e:
                self.app.log.error(e)
            self.app.log.info('Waiting for {0} seconds...'.format(self.app.config.get('plugin', 'duration')))
            time.sleep(int(self.app.config.get('plugin', 'duration')))

    def create_stat_sets(self):
        # Cement's config handler assumes there are unique name-values for everything.  That's not this kind of config.
        # Because config is an arbitrary list of endpoints to load, we'll have to handle this manually.
        all_endpoints = []
        endpoint_config = yaml.load(open(self.app.config.get('mlmonitor', 'endpoints_file')))
        for endpoint in endpoint_config['endpoints']:
            module = import_module('mlmonitor.core.stats.marklogic')
            component = getattr(module, endpoint['component'])()
            for key in endpoint.keys():
                if key != 'component':
                    if key == 'url':
                        value = '{0}://{1}:{2}@{3}:{4}{5}'.format(
                            self.app.config.get('marklogic', 'scheme'),
                            self.app.config.get('marklogic', 'user'),
                            self.app.config.get('marklogic', 'pass'),
                            self.app.config.get('marklogic', 'host'),
                            self.app.config.get('marklogic', 'port'),
                            endpoint[key]
                        )
                        setattr(component, key, value)
                        setattr(component, 'auth_scheme', self.app.config.get('marklogic', 'auth'))
                    else:
                        setattr(component, key, endpoint[key])
            all_endpoints.append(component)
        return all_endpoints
