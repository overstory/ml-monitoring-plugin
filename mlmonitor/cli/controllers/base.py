"""MarkLogic Monitoring Plugin base controller."""
import os
import traceback
from importlib import import_module

import time

import re
import yaml
import mlmonitor
from cement.ext.ext_argparse import ArgparseController, expose

from mlmonitor.core.utils.statsd_utils import StatsdUtility
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
                self.app.log.error(e, __name__)
                traceback.print_exc()
            self.app.log.info('Waiting for {0} seconds...'.format(self.app.config.get('plugin', 'duration')))
            time.sleep(int(self.app.config.get('plugin', 'duration')))

    def create_stat_sets(self):
        # Cement's config handler assumes there are unique name-values for everything.  That's not this kind of config.
        # Because config is an arbitrary list of endpoints to load, we'll have to handle this manually.
        all_endpoints = []
        endpoint_config = yaml.load(open(os.path.dirname(mlmonitor.__file__) + '/config/endpoints.yml'))

        # Load global stats.  These are consistent with all MarkLogic installations
        for endpoint in endpoint_config['endpoints']['global']:
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

        for endpoint in endpoint_config['endpoints']['configurable']:
            module = import_module('mlmonitor.core.stats.marklogic')

            # TODO: This assumes that every templated endpoint is going to have a property called "name" that is templated.  Not sure if that is valid in the long run
            for asset in self.find_assets(endpoint['name']):
                component = getattr(module, endpoint['component'])()
                # Assets are individual forest, database, server, group or hosts defined in the user configuration
                # Must iterate as there can by more than one
                for key in endpoint.keys():
                    if key != 'component':
                        if key == 'url':
                            value = '{0}://{1}:{2}@{3}:{4}{5}'.format(
                                self.app.config.get('marklogic', 'scheme'),
                                self.app.config.get('marklogic', 'user'),
                                self.app.config.get('marklogic', 'pass'),
                                self.app.config.get('marklogic', 'host'),
                                self.app.config.get('marklogic', 'port'),
                                self.replace_config_values(endpoint[key], asset))
                            setattr(component, key, value)
                            setattr(component, 'auth_scheme', self.app.config.get('marklogic', 'auth'))
                        else:
                            setattr(component, key, self.replace_config_values(endpoint[key], asset))
                all_endpoints.append(component)

        return all_endpoints

    def find_assets(self, string):
        pattern = '\[(\w+)\]'
        template = re.compile(pattern, re.UNICODE)
        match = template.search(string)
        if match:
            return self.app.config.get('plugin', match.group(1)).split(' ')
        else:
            return []

    def replace_config_values(self, string_to_alter, string_to_add):
        # Config values can be colon delimited.  If so, make sure we're replacing with each value
        value_set = string_to_add.split(":")
        pattern = '\[\w+\]'
        matches = re.findall(pattern, string_to_alter)
        for index, value in enumerate(value_set):
            if len(matches) > index:
                string_to_alter = string_to_alter.replace(matches[index], value)
        return string_to_alter
