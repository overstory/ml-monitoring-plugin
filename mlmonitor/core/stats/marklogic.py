import logging
from urlparse import urlparse

from mlmonitor.core.utils.http_utils import HTTPUtil
from mlmonitor.core.stats.base import StatSet, SimpleStatistic, StatisticType

log = logging.getLogger('cement:app:mlmonitor')

STATISTIC_UNITS_TO_IGNORE = ('bool', 'enum')


def generate_statistic_objects(prefix, dictionary, list_of_stats):
    """ Recursively prints nested dictionaries."""

    if isinstance(dictionary, list) and isinstance(dictionary[0], dict):
        generate_statistic_objects(prefix, dictionary[0], list_of_stats)
    else:
        for key, value in dictionary.items():
            if (prefix):
                new_prefix = prefix + "." + key
            else:
                new_prefix = key

            if isinstance(value, dict) or isinstance(value, list):
                generate_statistic_objects(new_prefix, value, list_of_stats)
            elif key == 'value':
                if (dictionary.get('units', None) and dictionary['units'] not in STATISTIC_UNITS_TO_IGNORE):
                    stat = SimpleStatistic(prefix, StatisticType.gauge, value, dictionary['units'])
                    log.debug("Adding SimpleStatistic: " + stat.__str__())
                    list_of_stats.append(stat)


class JsonRestStatSet(StatSet):
    def __init__(self, name=None, url=None, auth_scheme='DIGEST'):
        self._stats = []
        self.name = name
        self.url = url
        self.auth_scheme = auth_scheme

    @property
    def stats(self):
        return self._stats

    def calculate(self):
        url = urlparse(self.url)
        response = HTTPUtil.http_get(scheme='http', host=url.hostname, port=url.port, path=url.path + "?" + url.query,
                                     user=url.username, passwd=url.password, auth=self.auth_scheme)
        top_key_to_descend = response.values()[0]['status-list-summary'] if response.values()[0].get(
            'status-list-summary', None) else response.values()[0]['status-properties']

        generate_statistic_objects(self.name, top_key_to_descend, self._stats)
