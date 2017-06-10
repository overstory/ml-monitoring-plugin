import os
from unittest import TestCase

from bottle import response, Bottle

from mlmonitor.core.stats.marklogic import JsonRestStatSet
from mlmonitor.core.stats.base import STATISTIC_UNITS_TO_IGNORE, StatisticType
from tests.core.base import requires_http_server
import tests


class MarkLogicStatsCase(TestCase):
    host = '127.0.0.1'
    port = '8081'
    app = Bottle()

    @requires_http_server(app, host, port)
    def test_base_stat(self):
        @self.app.route('/forest/status')
        def forest_status():
            response.set_header('Content-Type', 'application/json')
            with open(os.path.dirname(tests.__file__) + '/resources/sample_forest_status_payload.json') as datafile:
                payload = datafile.read().replace('\n', '')
            return payload

        name = 'forest-status-list'
        url = 'http://{0}:{1}/forest/status'.format(self.host, self.port)

        stat_set = JsonRestStatSet(name, url)
        stat_set.calculate()

        self.assertEquals(stat_set.name, name)
        self.assertEquals(stat_set.url, url)

        self.assertEquals(stat_set.stats[0].name, 'forest-status-list.rate-properties.rate-detail.merge-write-rate')
        self.assertEquals(float(stat_set.stats[0].value), 1.37429594993591)
        self.assertEquals(stat_set.stats[0].unit, 'MB/sec')

        # Test to make sure none of the units on the excluded list
        for stat in stat_set.stats:
            self.assertNotIn(stat.unit, STATISTIC_UNITS_TO_IGNORE)
            if (stat.stat_type == StatisticType.timer):
                self.assertTrue(stat.statsd().endswith('s'))
            else:
                self.assertTrue(stat.statsd().endswith('g'))

    @requires_http_server(app, host, port)
    def test_stat_with_nested_payload(self):
        @self.app.route('/server/status')
        def server_status():
            response.set_header('Content-Type', 'application/json')
            with open(os.path.dirname(tests.__file__) + '/resources/sample_server_status_payload.json') as datafile:
                payload = datafile.read().replace('\n', '')
            return payload

        name = 'server-status'
        url = 'http://{0}:{1}/server/status'.format(self.host, self.port)

        server_stat_set = JsonRestStatSet(name, url)
        server_stat_set.calculate()

        self.assertEquals(server_stat_set.name, name)
        self.assertEquals(server_stat_set.url, url)

        self.assertEquals(len(server_stat_set.stats), 37)
        self.assertEquals(server_stat_set.stats[0].name, 'server-status.static-expires')
        self.assertEquals(server_stat_set.stats[0].unit, 'quantity')
        self.assertEquals(server_stat_set.stats[0].value, 3600)

    @requires_http_server(app, host, port)
    def test_stat_with_flat_payload(self):
        @self.app.route('/cluster/status')
        def server_status():
            response.set_header('Content-Type', 'application/json')
            with open(os.path.dirname(tests.__file__) + '/resources/sample_cluster_status_payload.json') as datafile:
                payload = datafile.read().replace('\n', '')
            return payload

        name = 'cluster-status'
        url = 'http://{0}:{1}/cluster/status'.format(self.host, self.port)

        server_stat_set = JsonRestStatSet(name, url)
        server_stat_set.calculate()

        self.assertEquals(server_stat_set.name, name)
        self.assertEquals(server_stat_set.url, url)

        # Looking for total-cpu stats
        had_total_cpu_stats = False
        for i in server_stat_set.stats:
            if 'total-cpu' in i.name :
                had_total_cpu_stats = True
        self.assertTrue(had_total_cpu_stats, "Did not find a SimpleStat object with total-cpu")
