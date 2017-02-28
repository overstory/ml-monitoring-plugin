import logging
import requests

from mlmonitor.core.stats.base import StatSet, SimpleStatistic, StatisticType

log = logging.getLogger('cement:app:mlmonitor')


def generate_statistic_objects(prefix, dictionary, list):
    """ Recursively prints nested dictionaries."""

    for key, value in dictionary.items():
        if (prefix):
            new_prefix = prefix + "." + key
        else:
            new_prefix = key

        if isinstance(value, dict):
            generate_statistic_objects(new_prefix, value, list)
        elif key == 'value':
            stat = SimpleStatistic(prefix, StatisticType.gauge, value, dictionary['units'])
            log.debug("Adding SimpleStatistic: " + stat.__str__())
            list.append(stat)


class JsonRestStatSet(StatSet):
    _stats = []

    def __init__(self, name, url):
        self.name = name
        self.url = url

    @property
    def stats(self):
        return self._stats

    def calculate(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            main_prefix = response.json().keys()[0]
            status_list_summary = response.json().values()[0]['status-list-summary']

            generate_statistic_objects(main_prefix, status_list_summary, self._stats)
        else:
            log.error("Response returned: {0} {1}".format(response.status_code, response.reason))
