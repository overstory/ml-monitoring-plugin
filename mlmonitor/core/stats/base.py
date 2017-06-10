import abc

import isodate
from enum import Enum

SUPPORTED_TIMER_UNITS = ('time', 'seconds')
STATISTIC_UNITS_TO_IGNORE = ('bool', 'enum', 'datetime')


class StatisticType(Enum):
    counter = 1
    timer = 2
    gauge = 3
    set = 4

    def datagram_format(stat_type):
        if stat_type == StatisticType.timer:
            return 's'
        else:
            return stat_type.name[0:1]


class BaseStatistic(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def newrelic(self):
        return

    @abc.abstractmethod
    def statsd(self):
        return


class SimpleStatistic(BaseStatistic):
    def __init__(self, name, value=0, unit=None):
        self.name = name
        self.value = value
        self.unit = unit

        if unit in SUPPORTED_TIMER_UNITS:
            self.stat_type = StatisticType.timer
        else:
            self.stat_type = StatisticType.gauge

    def __str__(self):
        return "{0}: {1} {2}".format(self.name, self.value, self.unit)

    def newrelic(self):
        if self.stat_type == StatisticType.timer:
            value = isodate.parse_duration(self.value).total_seconds()
        else:
            value = self.value
        return {"Component/{0}[{1}]".format(self.name.replace(".", "/"), self.unit):value}

    def statsd(self):
        if self.stat_type == StatisticType.timer:
            value = isodate.parse_duration(self.value).total_seconds()
        else:
            value = self.value
        return "{0}:{1}|{2}".format(self.name, value, StatisticType.datagram_format(self.stat_type))


class StatSet(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def stats(self):
        # A list/iterable that only contains BaseStatistic objects
        return []

    @abc.abstractmethod
    def calculate(self):
        # Make sure all implementations populate their own stats property
        return
