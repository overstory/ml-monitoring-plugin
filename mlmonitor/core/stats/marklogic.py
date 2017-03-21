import logging
from urlparse import urlparse

from mlmonitor.core.utils.http_utils import HTTPUtil
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

    def __init__(self, name=None, url=None, auth_scheme='DIGEST'):
        self.name = name
        self.url = url
        self.auth_scheme = auth_scheme

    @property
    def stats(self):
        return self._stats

    def calculate(self):
        url = urlparse(self.url)
        response = HTTPUtil.http_get(scheme='http', host=url.hostname, port=url.port, path=url.path + "?" + url.query, user = url.username, passwd=url.password, auth=self.auth_scheme)
        status_list_summary = response.values()[0]['status-list-summary']

        generate_statistic_objects(self.name, status_list_summary, self._stats)