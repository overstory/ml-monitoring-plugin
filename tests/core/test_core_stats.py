from unittest import TestCase

import isodate

from mlmonitor.core.stats.base import SimpleStatistic, StatisticType


class CoreStatsTest(TestCase):
    def test_base_stat(self):
        name = 'stat.name'
        type = StatisticType.gauge
        value = 1
        unit = 'sec/sec'

        stat = SimpleStatistic(name, value, unit)
        self.assertEquals(stat.name, name)
        self.assertEquals(stat.stat_type, type)
        self.assertEquals(stat.value, value)

        datagram = "{0}:{1}|{2}".format(name, value, 'g')
        nr_component_stat = {"Component/{0}[{1}]".format(name.replace(".", "/"), unit): value}

        self.assertEquals(datagram, stat.statsd())
        self.assertEquals(nr_component_stat, stat.newrelic())

    def test_timer_stat(self):
        name = 'stat.timer'
        type = StatisticType.timer
        value = 'PT3M17.863547S'
        unit = 'seconds'

        stat = SimpleStatistic(name, value, unit)
        self.assertEquals(stat.name, name)
        self.assertEquals(stat.stat_type, type)
        self.assertEquals(stat.value, value)

        display_value = isodate.parse_duration(value).total_seconds()

        datagram = "{0}:{1}|{2}".format(name, display_value, 's')

        self.assertEquals(datagram, stat.statsd())
