#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016 MarkLogic Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0#
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
__init__.py module entry point for running plugin

"""

import json
import logging
import re
import time
import traceback

__version__ = '0.3'

from mlmonitor.core.utils import newrelic_utils
from mlmonitor.core.marklogic.marklogic_status import MarkLogicStatus

log = logging.getLogger('cement:app:mlmonitor')


class RunPlugin:
    def __init__(self, config=None):

        # setup configuration
        self.config = config

        log.debug('parse config')
        log.debug(config.get('marklogic', 'host'))
        self.ml_host = config.get('marklogic', 'host')
        self.ml_port = config.getint('marklogic', 'port')
        self.ml_url = "http://" + self.ml_host + ":"
        self.ml_url += repr(self.ml_port)
        log.debug(self.ml_url)
        self.ml_user = config.get('marklogic', 'user')
        self.ml_pass = config.get('marklogic', 'pass')
        self.ml_scheme = config.get('marklogic', 'scheme')
        self.ml_auth = config.get('marklogic', 'auth')
        self.nr_license_key = config.get('newrelic', 'key')
        self.nr_http_proxy = config.get('newrelic', 'http_proxy')
        self.plugin_name = config.get('plugin', 'name')
        self.plugin_guid = config.get('plugin', 'guid')
        self.plugin_duration = config.getint('plugin', 'duration')
        self.plugin_summary_status = config.getboolean('plugin', 'summary_status')
        self.plugin_databases = config.get('plugin', 'databases')
        self.plugin_hosts_summary_status = config.getboolean('plugin', 'hosts_summary_status')
        self.plugin_hosts = config.get('plugin', 'hosts')
        self.plugin_forests_summary_status = config.getboolean('plugin', 'forests_summary_status')
        self.plugin_forests = config.get('plugin', 'forests')
        self.plugin_groups = config.get('plugin', 'groups')
        self.plugin_servers_summary_status = config.getboolean('plugin', 'servers_summary_status')
        self.plugin_servers = config.get('plugin', 'servers')

    def run(self):
        log.info(
            "newrelic_marklogic plugin now sending statuses to NewRelic Plugin API (to see more log messages change level=debug).")
        while True:
            try:
                self.statusUpdate()
            except Exception as e:
                log.error(e)
                traceback.print_exc()
            time.sleep(self.plugin_duration)

    def statusUpdate(self):
        log.debug("retrieve statuses and update newrelic")
        status = MarkLogicStatus(scheme=self.ml_scheme, user=self.ml_user, passwd=self.ml_pass, auth=self.ml_auth,
                                 host=self.ml_host, port=self.ml_port
                                 )
        metrics = {}

        # retrieve summary status
        if self.plugin_summary_status:
            cluster_status = status.get()
            forest_summary = cluster_status['local-cluster-status']['status-relations']['forests-status'][
                'forests-status-summary']
            for metric in forest_summary:
                if metric == 'cache-properties':
                    cache_properties = forest_summary['cache-properties']
                    for cp in cache_properties:
                        metrics["Component/forests/cache/" + cp + "[" + cache_properties[cp]["units"] + "]"] = \
                            cache_properties[cp]["value"]
                else:
                    metrics["Component/forests/" + metric + "[" + forest_summary[metric]["units"] + "]"] = \
                        forest_summary[metric]["value"]

            request_summary = cluster_status['local-cluster-status']['status-relations']['requests-status'][
                'requests-status-summary']
            for metric in request_summary:
                metrics["Component/requests/" + metric + "[" + request_summary[metric]["units"] + "]"] = \
                    request_summary[metric]["value"]

            transaction_summary = cluster_status['local-cluster-status']['status-relations']['transactions-status'][
                'transactions-status-summary']
            for metric in transaction_summary:
                metrics["Component/transactions/" + metric + "[" + transaction_summary[metric]["units"] + "]"] = \
                    transaction_summary[metric]["value"]

            server_summary = cluster_status['local-cluster-status']['status-relations']['servers-status'][
                'servers-status-summary']
            for metric in server_summary:
                metrics["Component/servers/" + metric + "[" + server_summary[metric]["units"] + "]"] = \
                    server_summary[metric]["value"]

            host_summary = cluster_status['local-cluster-status']['status-relations']['hosts-status'][
                'hosts-status-summary']
            for metric in host_summary:
                if metric == 'load-properties':
                    metrics["Component/hosts/load/total-load[" + host_summary[metric]["total-load"]["units"] + "]"] = \
                        host_summary[metric]["total-load"]["value"]
                    for ld in host_summary[metric]["load-detail"]:
                        metrics["Component/hosts/load/detail/" + ld + "[" + host_summary[metric]["load-detail"][ld][
                            "units"] + "]"] = \
                            host_summary[metric]["load-detail"][ld]["value"]
                elif metric == 'rate-properties':
                    metrics["Component/hosts/rate/total-rate[" + host_summary[metric]["total-rate"]["units"] + "]"] = \
                        host_summary[metric]["total-rate"]["value"]
                    for lr in host_summary[metric]["rate-detail"]:
                        metrics["Component/hosts/rate/detail/" + lr + "[" + host_summary[metric]["rate-detail"][lr][
                            "units"] + "]"] = \
                            host_summary[metric]["rate-detail"][lr]["value"]
                else:
                    metrics["Component/hosts/" + metric + "[" + host_summary[metric]["units"] + "]"] = \
                        host_summary[metric]["value"]

        # retrieve forest summary status
        if self.plugin_forests_summary_status:
            forest_status = status.get(resource="forests")
            forest_summary = forest_status['forest-status-list']['status-list-summary']
            for metric in forest_summary:
                if metric == 'cache-properties':
                    cache_properties = forest_summary['cache-properties']
                    for cp in cache_properties:
                        metrics["Component/forests/cache/" + cp + "[" + cache_properties[cp]["units"] + "]"] = \
                            cache_properties[cp]["value"]
                elif metric == 'load-properties':
                    load_properties = forest_summary['load-properties']
                    metrics["Component/forests/load/total-load[" + load_properties["total-load"]["units"] + "]"] = \
                        load_properties["total-load"]["value"]
                    load_details = load_properties["load-detail"]
                    for ld in load_details:
                        metrics["Component/forests/load/detail/" + ld + "[" + load_details[ld]["units"] + "]"] = \
                            load_details[ld]["value"]
                elif metric == 'rate-properties':
                    rate_properties = forest_summary['rate-properties']
                    metrics["Component/forests/rate/total-rate[" + rate_properties["total-rate"]["units"] + "]"] = \
                        rate_properties["total-rate"]["value"]
                    rate_details = rate_properties["rate-detail"]
                    for rd in rate_details:
                        metrics["Component/forests/rate/detail/" + rd + "[" + rate_details[rd]["units"] + "]"] = \
                            rate_details[rd]["value"]
                else:
                    metrics["Component/forests/" + metric + "[" + forest_summary[metric]["units"] + "]"] = \
                        forest_summary[metric]["value"]

        # retrieve host summary status
        if self.plugin_hosts_summary_status:
            host_status = status.get(resource="hosts")
            host_summary = host_status['host-status-list']['status-list-summary']
            for metric in host_summary:
                if metric == 'load-properties':
                    metrics[
                        "Component/hosts/load/total-load[" + host_summary[metric]["total-load"]["units"] + "]"] = \
                        host_summary[metric]["total-load"]["value"]
                    for ld in host_summary[metric]["load-detail"]:
                        metrics["Component/hosts/load/detail/" + ld + "[" + host_summary[metric]["load-detail"][ld][
                            "units"] + "]"] = \
                            host_summary[metric]["load-detail"][ld]["value"]

                elif metric == 'rate-properties':
                    metrics[
                        "Component/hosts/rate/total-rate[" + host_summary[metric]["total-rate"]["units"] + "]"] = \
                        host_summary[metric]["total-rate"]["value"]
                    for lr in host_summary[metric]["rate-detail"]:
                        metrics["Component/hosts/rate/detail/" + lr + "[" + host_summary[metric]["rate-detail"][lr][
                            "units"] + "]"] = \
                            host_summary[metric]["rate-detail"][lr]["value"]
                else:
                    metrics["Component/hosts/" + metric + "[" + host_summary[metric]["units"] + "]"] = \
                        host_summary[metric]["value"]

        # retrieve server summary status
        if self.plugin_servers_summary_status:
            server_status = status.get(resource="servers")
            server_summary = server_status['server-status-list']['status-list-summary']
            for ss in server_summary:
                metrics["Component/servers/" + ss + "[" + server_summary[ss]["units"] + "]"] = \
                    server_summary[ss]["value"]

        # retrieve specific database detail status
        if self.plugin_databases:
            for db in re.split(" ", self.plugin_databases):
                database_status = status.get(resource="databases", name=db)
                database_detail = database_status["database-status"]["status-properties"]
                for dd in database_detail:
                    units = None
                    if "units" in database_detail[dd]:
                        units = database_detail[dd]["units"]
                    if dd == "load-properties":
                        database_load_details = \
                        database_status["database-status"]["status-properties"]["load-properties"]["load-detail"]
                        for dld in database_load_details:
                            load_units = None
                            if "units" in database_load_details[dld]:
                                load_units = database_load_details[dld]["units"]
                            if not load_units:
                                metrics["Component/databases/" + db + "/load/" + dld] = database_load_details[dld]
                            else:
                                metrics["Component/databases/" + db + "/load/" + dld + "[" + load_units + "]"] = \
                                    database_load_details[dld]["value"]
                    elif dd == "rate-properties":
                        database_rate_details = \
                        database_status["database-status"]["status-properties"]["rate-properties"]["rate-detail"]
                        for drd in database_rate_details:
                            rate_units = None
                            if "units" in database_rate_details[drd]:
                                rate_units = database_rate_details[drd]["units"]
                            if not rate_units:
                                metrics["Component/databases/" + db + "/rate/" + drd] = database_rate_details[drd]
                            else:
                                metrics["Component/databases/" + db + "/rate/" + drd + "[" + rate_units + "]"] = \
                                    database_rate_details[drd]["value"]
                    elif dd == "cache-properties":
                        database_cache_details = \
                            database_status["database-status"]["status-properties"]["cache-properties"]
                        for dcd in database_cache_details:
                            cache_units = None
                            if "units" in database_cache_details[dcd]:
                                cache_units = database_cache_details[dcd]["units"]
                            if not cache_units:
                                metrics["Component/databases/" + db + "/cache/" + dcd] = database_cache_details[dcd]
                            else:
                                metrics["Component/databases/" + db + "/cache/" + dcd + "[" + cache_units + "]"] = \
                                    database_cache_details[dcd]["value"]
                    elif re.match(
                            "local-disk-failover|database-replication-status|flexible-replication-enabled|cpf-enabled",
                            dd):
                        log.debug("ignoring " + dd)
                    elif not units:
                        metrics["Component/databases/" + db + "/" + dd] = database_detail[dd]
                    else:
                        metrics["Component/databases/" + db + "/" + dd + "[" + units + "]"] = \
                            database_detail[dd]["value"]

        # retrieve specific host detail status
        if self.plugin_hosts:
            metrics.update(self.getHostDetailStatus(status, self.plugin_hosts))
        # retrieve specific forest detail status
        if self.plugin_forests:
            metrics.update(self.getForestDetailStatus(status, self.plugin_forests))

        # retrieve specific group detail status
        if self.plugin_groups:
            metrics.update(self.getGroupDetailStatus(status, self.plugin_groups))

        # retrieve specific server detail status
        if self.plugin_servers:
            metrics.update(self.getServerDetailStatus(status, self.plugin_servers))

        update_newrelic = newrelic_utils.NewRelicUtility.update_newrelic(self,
                                                                         host=self.ml_host,
                                                                         pid=1,
                                                                         version=__version__,
                                                                         name=self.plugin_name,
                                                                         guid=self.plugin_guid,
                                                                         duration=self.plugin_duration,
                                                                         metrics=metrics,
                                                                         key=self.nr_license_key,
                                                                         proxy=self.nr_http_proxy)

        if "error" in update_newrelic:
            log.error(update_newrelic["error"])
        else:
            log.debug("update status: " + json.dumps(update_newrelic))

    def getHostDetailStatus(self, status, hosts):
        metrics = {}
        for host in re.split(" ", hosts):
            host_status = status.get(resource="hosts", name=host)
            host_detail = host_status["host-status"]["status-properties"]
            for hd in host_detail:
                if re.match("online|secure", hd):
                    log.debug("ignoring " + hd)
                elif hd == "load-properties":
                    host_load_details = \
                        host_status["host-status"]["status-properties"]["load-properties"]["load-detail"]
                    for hld in host_load_details:
                        load_units = None
                        if "units" in host_load_details[hld]:
                            load_units = host_load_details[hld]["units"]
                        if not load_units:
                            metrics["Component/hosts/" + host + "/load/" + hld] = host_load_details[hld]
                        else:
                            metrics["Component/hosts/" + host + "/load/" + hld + "[" + load_units + "]"] = \
                                host_load_details[hld]["value"]
                elif hd == "rate-properties":
                    host_rate_details = \
                        host_status["host-status"]["status-properties"]["rate-properties"]["rate-detail"]
                    for hrd in host_rate_details:
                        rate_units = None
                        if "units" in host_rate_details[hrd]:
                            rate_units = host_rate_details[hrd]["units"]
                        if not rate_units:
                            metrics["Component/hosts/" + host + "/rate/" + hrd] = host_rate_details[hrd]
                        else:
                            metrics["Component/hosts/" + host + "/rate/" + hrd + "[" + rate_units + "]"] = \
                                host_rate_details[hrd]["value"]
                elif hd == "status-detail":
                    host_status_detail = host_detail["status-detail"]
                    for hsd in host_status_detail:
                        units = None
                        try:
                            if 'units' in host_status_detail[hsd]:
                                units = host_status_detail[hsd]["units"]
                        except Exception as e:
                            log.debug("has no units " + hsd)
                        if re.match("license-key-options", hsd):
                            log.debug("ignoring " + hsd)
                        elif not units:
                            metrics["Component/hosts/" + host + "/" + hsd] = host_detail["status-detail"][hsd]
                        else:
                            metrics["Component/hosts/" + host + "/" + hsd + "[" + units + "]"] = \
                                host_status_detail[hsd]["value"]
            return metrics

    def getForestDetailStatus(self, status, forests):
        metrics = {}
        for forest in re.split(" ", forests):
            forest_status = status.get(resource="forests", name=forest)
            forest_detail = forest_status["forest-status"]["status-properties"]
            for fd in forest_detail:
                units = None
                if "units" in forest_detail[fd]:
                    units = forest_detail[fd]["units"]
                if re.match("license-key-options|unclosed-stands|stands", fd):
                    log.debug("ignoring " + fd)
                elif not units:
                    metrics["Component/forests/" + forest + "/" + fd] = forest_detail[fd]
                else:
                    metrics["Component/forests/" + forest + "/" + fd + "[" + units + "]"] = \
                        forest_detail[fd]["value"]
            return metrics

    def getGroupDetailStatus(self, status, groups):
        metrics = {}
        for group in re.split(" ", groups):
            group_status = status.get(resource="groups", name=group)
            group_detail = group_status["group-status"]["status-properties"]
            for gd in group_detail:
                units = None
                if "units" in group_detail[gd]:
                    units = group_detail[gd]["units"]
                if gd == "hosts-status-summary":
                    metrics["Component/groups/" + group + "/hosts/total-hosts[quantity]"] = \
                        group_detail["hosts-status-summary"]["total-hosts"]["value"]
                elif gd == "servers-status-properties":
                    log.debug("ignoring group servers-status-properties")
                elif gd == "servers-status-summary":
                    log.debug("ignoring group servers-status-summary")
                else:
                    log.debug("ignoring group " + gd)
            return metrics

    def getServerDetailStatus(self, status, servers):
        metrics = {}
        for servergroup in re.split(" ", servers):
            s = servergroup.split(":")
            server = s[0]
            group = s[1]
            if server and group:
                server_status = status.get(resource="servers", name=server, group=group)
                server_detail = server_status["server-status"]["status-properties"]
                for sd in server_detail:
                    units = None
                    try:
                        if "units" in server_detail[sd]:
                            units = server_detail[sd]["units"]
                    except Exception as e:
                        log.debug("has no units " + sd)
                    if sd == "host-detail":
                        server_host_details = \
                            server_status["server-status"]["status-properties"]["host-detail"]
                        for shd in server_host_details:
                            log.debug(shd)
                            # host_units = None
                            # if "units" in server_host_details[shd]:
                            #     host_units = server_host_details[shd]["units"]
                            # if re.match("relation-id|url-rewriter", shd):
                            #     log.debug("ignoring " + shd)
                            # elif not host_units:
                            #     metrics["Component/servers/" + server + "/host/" + shd] = server_host_details[shd]
                            # else:
                            #     metrics["Component/servers/" + server + "/host/" + shd + "[" + host_units + "]"] = \
                            #         server_host_details[shd]["value"]
                    elif re.match("root|output-encoding|error-handler|url-rewriter", sd):
                        log.debug("ignoring " + sd)
                    elif not units:
                        metrics["Component/servers/" + server + "/" + sd] = server_detail[sd]
                    else:
                        metrics["Component/servers/" + server + "/" + sd + "[" + units + "]"] = \
                            server_detail[sd]["value"]
                return metrics
            else:
                log.error("cannot retrieve " + server + " server status, check configuration")
