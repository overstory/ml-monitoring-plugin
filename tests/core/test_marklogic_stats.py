import os
from mlmonitor.core.stats.marklogic import JsonRestStatSet
from tests.core.base import ServeredTestCase
from bottle import response


class MarkLogicStatsCase(ServeredTestCase):
    def setUp(self):
        super(MarkLogicStatsCase, self).setUp()
        app = super(MarkLogicStatsCase, self).app

        @app.route('/forest/status')
        def forest_status():
            response.set_header('Content-Type', 'application/json')
            with open(os.path.dirname(os.path.realpath('__file__')) + '/resources/sample_forest_status_payload.json') as datafile:
                payload = datafile.read().replace('\n', '')
            return payload

    def test_base_stat(self):
        name = 'test stat set'
        url = 'http://127.0.0.1:8080/forest/status'

        stat_set = JsonRestStatSet(name, url)
        stat_set.calculate()

        self.assertEquals(stat_set.name, name)
        self.assertEquals(stat_set.url, url)

        self.assertEquals(stat_set.stats[0].name, 'forest-status-list.rate-properties.rate-detail.merge-write-rate')
        self.assertEquals(float(stat_set.stats[0].value), 1.37429594993591)
        self.assertEquals(stat_set.stats[0].unit, 'MB/sec')
