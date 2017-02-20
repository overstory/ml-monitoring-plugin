from unittest import TestCase
from mlmonitor.core.stats.core import SimpleStatistic, StatisticType


class CoreStatsTest(TestCase):
    def test_base_stat(self):
        name = 'stat.name'
        type = StatisticType.counter
        value = 1

        stat = SimpleStatistic(name, type, value)
        self.assertEquals(stat.name, name)
        self.assertEquals(stat.stat_type, type)
        self.assertEquals(stat.value, value)

        datagram = "{0}:{1}|{2}".format(name, value, 'c')

        self.assertEquals(datagram, stat.statsd())

    def test_timer_stat(self):
        name = 'stat.timer'
        type = StatisticType.timer
        value = 1

        stat = SimpleStatistic(name, type, value)
        self.assertEquals(stat.name, name)
        self.assertEquals(stat.stat_type, type)
        self.assertEquals(stat.value, value)

        datagram = "{0}:{1}|{2}".format(name, value, 'ms')

        self.assertEquals(datagram, stat.statsd())
