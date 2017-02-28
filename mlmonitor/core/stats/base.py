from enum import Enum
import abc


class StatisticType(Enum):
    counter = 1
    timer = 2
    gauge = 3
    set = 4

    def datagram_format(stat_type):
        if stat_type == StatisticType.timer:
            return 'ms'
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
    def __init__(self, name, stat_type, value=0, unit=None):
        self.name = name
        self.stat_type = stat_type
        self.value = value
        self.unit = unit

    def __str__(self):
        return "{0}: {1} {2}".format(self.name, self.value, self.unit)

    def newrelic(self):
        raise NotImplementedError

    def statsd(self):
        return "{0}:{1}|{2}".format(self.name, self.value, StatisticType.datagram_format(self.stat_type))


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
