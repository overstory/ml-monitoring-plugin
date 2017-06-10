import logging
from urlparse import urlparse

from mlmonitor.core.stats.base import STATISTIC_UNITS_TO_IGNORE
from mlmonitor.core.stats.base import StatSet, SimpleStatistic
from mlmonitor.core.utils.http_utils import HTTPUtil

log = logging.getLogger('cement:app:mlmonitor')


def generate_statistic_objects(prefix, dictionary, list_of_stats):
    """ Recursively prints nested dictionaries."""

    if isinstance(dictionary, list) and isinstance(dictionary[0], dict):
        generate_statistic_objects(prefix, dictionary[0], list_of_stats)
    elif hasattr(dictionary, 'keys') and 'stand-id' in dictionary.keys():
        stand_id = dictionary.pop('stand-id', None)[0]
        generate_statistic_objects(prefix + "." + stand_id, dictionary, list_of_stats)
    elif hasattr(dictionary, 'keys'):
        for key, value in dictionary.items():
            if (prefix):
                new_prefix = prefix + "." + key
            else:
                new_prefix = key

            if isinstance(value, dict) or isinstance(value, list):
                generate_statistic_objects(new_prefix, value, list_of_stats)
            elif key == 'value' or isinstance(value, int) or isinstance(value, float):
                if dictionary.get('units', None) and dictionary['units'] not in STATISTIC_UNITS_TO_IGNORE:
                    stat = SimpleStatistic(prefix, value, dictionary['units'])
                    log.debug("Adding SimpleStatistic: " + stat.__str__())
                    list_of_stats.append(stat)
                elif dictionary.get('units', None) is None and 'total-cpu' in new_prefix:
                    stat = SimpleStatistic(new_prefix, value, '%')
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
        top_key_to_descend = response.values()[0].get('status-list-summary', None)

        if top_key_to_descend is None and response.values()[0].get('status-properties', None) is not None:
            top_key_to_descend = response.values()[0]['status-properties']
        elif top_key_to_descend is None and response.values()[0].get('status-relations', None) is not None:
            top_key_to_descend = response.values()[0]['status-relations']

        generate_statistic_objects(self.name, top_key_to_descend, self._stats)
