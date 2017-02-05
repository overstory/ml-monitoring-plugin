newrelic-marklogic-plugin
=========================

`NewRelic <http://www.newrelic.com>`__ plugin for monitoring
MarkLogic.

Features
--------

-  Easy to install as pip or rpm
-  Configurable selection of metrics to retrieve
-  Retrieve summary metrics on local cluster, hosts, servers & forests.
-  Retrieve detail metrics on databases, forests, hosts, groups & servers.
-  Proxy access to NewRelic api
-  Sample monitoring dashboards available at `NewRelic plugin central <https://newrelic.com/plugins>`__.

Before you start
----------------

Require minimally `Python 2.7.10  <https://www.python.org/>`__ installed.

Require minimally `MarkLogic v7.0-6 <http://developer.marklogic.com/products>`__ installed
and running.

Require `NewRelic <http://www.newrelic.com/>`__ account.

Docs
----

`newrelic-marklogic-plugin docs on github <https://github.com/marklogic/newrelic-plugin>`__

`newrelic-marklogic-plugin docs on pypi <https://pypi.python.org/pypi/newrelic-marklogic-plugin>`__

Build
-----

A pure python package can be build by running
``python setup.py clean bdist_wheel

rpm package can be build by running
``python setup.py clean bdist_rpm



Install, configure & run
------------------------

Install the plugin using any of the following methods.

- install from pypi repository

    ``pip install newrelic-marklogic-plugin``

- install as rpm

    ``yum localinstall -y mlmonitor-0.3-0.1.noarch.rpm

- install direct from github

    ``pip install https://github.com/marklogic/newrelic-plugin/archive/master.zip``

- download `release <https://github.com/marklogic/newrelic-plugin/releases>`__  (or clone) repository and run the following.

    ``python setup.py install``


Next step is to create and edit configuration file.

1) Copy
   `etc/newrelic\_marklogic.conf.sample <https://github.com/marklogic/newrelic-plugin/blob/master/etc/newrelic_marklogic.conf.sample>`__
   and to ``mlmonitor.conf``

2) Edit ``mlmonitor.conf`` ensuring correct MarkLogic
   connection details and NewRelic license key

Start reporting metrics to NewRelic by running the following.

    ``ml-monitoring-plugin/mlmonitor/cli/main.py -c newrelic_marklogic.conf``

Which samples metrics every period of length duration as set within configuration.

It is recommended to initiate plugin as a background task, run via a scheduler (ex. cron job) or using any other
approach appropriate for your environment.

Running with -h flag will emit usage instructions for running plugin.

    ``ml-monitoring-plugin/mlmonitor/cli/main.py -h``

::

    usage: mlmonitor [-h] [--debug] [--quiet] [--daemon] [-c CONFIG]
                 {newrelic} ...

    Universal monitoring plugin for MarkLogic

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output
      --daemon    daemonize the process
      -c CONFIG   Location of config file to parse

    sub-commands:
      {newrelic}
        newrelic  Starts up process to monitor MarkLogic with New Relic

Usage
-----

The configuration file drives all newrelic-marklogic-plugin features and is split into several sections.

The 'marklogic' section contains connection details to MarkLogic server and Management REST API.

::

    [marklogic]

    # Scheme to use when accessing MarkLogic management REST API (http|https).
    scheme = http

    # Host to use when accessing MarkLogic management REST API (FQDN hostname).
    host = localhost

    # Port to use when accessing MarkLogic management REST API.
    port = 8002

    # Authentication to use when accessing MarkLogic management REST API (BASIC|DIGEST).
    auth= DIGEST

    # Username to use when accessing MarkLogic management REST API.
    user = admin

    # Password to use when accessing MarkLogic management REST API.
    pass = admin

The 'newrelic' section specifies the NewRelic license key. Optionally you may nominate a proxy for accessing the NewRelic Plugin API.

::

    [newrelic]

    # Your NewRelic license key.
    key = ****************************************

    # Proxy (ex. http://10.10.1.10:3128).
    http_proxy =

The 'plugin' section defines sample period for updating NewRelic, as well as the logging level for emitting messages about plugin operation.

There are a set of configurations for defining which statuses are captured by NewRelic, summarised below.

- summary_status (True|False): retrieve local cluster summary status.
- databases (list of databases): retrieve database detailed status.
- hosts_summary_status (True|False):  retrieve summary of all hosts status.
- hosts (list of hosts): retrieve host detailed status.
- forests_summary_status (True|False): retrieve summary of all forests status.
- forests (list of forests): retrieve forest detailed status.
- groups (list of groups): retrieve group detailed status.
- servers_summary_status (True|False): retrieve summary of all servers status.
- servers (list of servers): retrieve server detailed status.

::

    [plugin]

    # NewRelic plugin display name.
    name = marklogic

    # Unique NewRelic plugin guid.
    guid = com.marklogic

    # Sample period in seconds.
    duration = 60

    # Set logging level (INFO|DEBUG|ERROR).
    log_level = DEBUG

    # Local cluster summary.
    summary_status= False

    # Database(s) detail status.
    databases= Documents

    # Hosts summary.
    hosts_summary_status= True

    # Host(s) detail status.
    hosts= 127.0.0.1

    # Forests summary.
    forests_summary_status= True

    # Forest(s) detail status.
    forests= Documents Meters

    # Group(s) detail status.
    groups= Default

    # Servers summary.
    servers_summary_status= True

    # Server(s) detail status (must supply group name ex. ServerName:GroupName).
    servers= Manage:Default

Issues, feature requests & contributing
---------------------------------------

Please file `bug reports <https://github.com/marklogic/newrelic-plugin/issues>`__, `feature
requests <https://github.com/marklogic/newrelic-plugin/issues>`__, and contribute with `pull
requests <https://github.com/marklogic/newrelic-plugin/pulls>`__ through GitHub.

Copyright & License
-------------------

newrelic-marklogic-plugin Copyright 2016 MarkLogic Corporation

newrelic-marklogic-plugin is licensed under the Apache License, Version 2.0 (the "License"),
a copy of the license is included within this package.

`Apache License v2.0 <https://github.com/marklogic/newrelic-plugin/blob/master/LICENSE>`__