import os
from unittest import TestCase

from bottle import response, Bottle

from mlmonitor.core.stats.marklogic import JsonRestStatSet
from tests.core.base import requires_http_server


class MarkLogicStatsCase(TestCase):
    host = '127.0.0.1'
    port = '8081'
    app = Bottle()

    @requires_http_server(app, host, port)
    def test_base_stat(self):
        @self.app.route('/forest/status')
        def forest_status():
            response.set_header('Content-Type', 'application/json')
            with open(os.path.dirname(
                    os.path.realpath('__file__')) + '/resources/sample_forest_status_payload.json') as datafile:
                payload = datafile.read().replace('\n', '')
            return payload

        name = 'test stat set'
        url = 'http://{0}:{1}/forest/status'.format(self.host, self.port)

        stat_set = JsonRestStatSet(name, url)
        stat_set.calculate()

        self.assertEquals(stat_set.name, name)
        self.assertEquals(stat_set.url, url)

        self.assertEquals(stat_set.stats[0].name, 'forest-status-list.rate-properties.rate-detail.merge-write-rate')
        self.assertEquals(float(stat_set.stats[0].value), 1.37429594993591)
        self.assertEquals(stat_set.stats[0].unit, 'MB/sec')
