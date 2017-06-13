AutoPilot CE -- A MarkLogic Monitoring Plugin
=
Universal monitoring plugin that supports multiple statistics backends. Heavily inspired by [MarkLogic's own New Relic plugin](https://github.com/marklogic/newrelic-plugin).

Features
-

-  Built on the [Cement Framework](http://builtoncement.com) for command line tools.
-  Easy to install as pip or rpm.
-  Configurable selection of metrics to retrieve.
-  Retrieve summary metrics on local cluster, hosts, servers & forests.
-  Retrieve detail metrics on databases, forests, hosts, groups & servers.
-  Default dashboard on New Relic, focusing on Speed, IO, Locks and Storage.

Requirements
-

- [Python 2.7.10](https://www.python.org).  Does not currently support 2.6 or earlier nor 3.0 or higher.

- [MarkLogic v7.0-6](http://developer.marklogic.com/products) or later installed
and running.

- Either a valid [New Relic](https://newrelic.com) account or a StatsD-compliant collector such as [DataDog](https://github.com/DataDog/dd-agent), [Telegraf](https://github.com/influxdata/telegraf) or [StatsD](https://github.com/etsy/statsd) itself.

Build
-

From the root diretory of this repository, download necessary dependencies for building and running

    > pip install -r requirements.txt

A pure python package can be built by running
    
    > python setup.py clean bdist_wheel

An rpm package can be built by running
    
    > python setup.py clean bdist_rpm


Tests
-

Tests are designed and run with `nose2` but should be `unittest` and `nose` compliant. Please run tests from `tests` directory.
    

Installation 
-

Installation is supported from a locally accessible version of a build (support from PyPI is coming soon). You can download the
latest release [here](https://github.com/overstory/ml-monitoring-plugin/releases/download/0.3/mlmonitor-0.3-py2.py3-none-any.whl).

From a python package:

    > pip install mlmonitor-0.3-py2.py3-none-any.whl
    
From an rpm file:

    > yum localinstall -y mlmonitor-0.3-0.1.noarch.rpm



Configuration 
-

``config/mlmonitor.conf`` is required by the module to setup sensible defaults.  You are required to have a local copy to include 
your own configuration values. *Do not edit ``config/mlmonitor.conf`` directly*.

1) Copy ``config/marklogic.conf`` to a local copy and place it in ``~/.mlmonitor/application.conf``. Alternatively, the local
copy of the configuration file can be specified using the -c parameter when executing its command.

2) Edit ``application.conf``.  Please see the [Usage](#usage) section for more details
    

Running
-

It is recommended to initiate plugin as a background task, run via a scheduler (ex. cron job) or using any other
approach appropriate for your environment.

Running with -h flag will emit usage instructions for running plugin.

    > mlmonitor -h


    usage: mlmonitor [-h] [--debug] [--quiet] [--daemon] [-c CONFIG]
                     {newrelic,statsd} ...
  
    Universal monitoring plugin for MarkLogic
    
    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      --daemon           daemonize the process
      -c CONFIG          Location of config file to parse
    
    sub-commands:
      {newrelic,statsd}
        newrelic         Starts up process to send status update from MarkLogic to
                         New Relic
        statsd           Starts up process to send status update from MarkLogic to
                         StatsD
                         
 Example
 
    > mlmonitor -c /tmp/application.conf newrelic



<a name="usage">Usage</a>
-----

The configuration file drives all AutoPilotCE features and is split into several sections.

The 'marklogic' section contains connection details to MarkLogic server and Management REST API.

    [marklogic]
    
    # Scheme to use when accessing MarkLogic management REST API (http|https).
    scheme = http
    
    # Host to use when accessing MarkLogic management REST API (FQDN hostname).
    host = <HOSTNAME>
    
    # Port to use when accessing MarkLogic management REST API.  Usually 8002
    port = 8002
    
    # Authentication to use when accessing MarkLogic management REST API (BASIC|DIGEST).
    auth= DIGEST
    
    # Username to use when accessing MarkLogic management REST API.
    user = <USERNAME>
    
    # Password to use when accessing MarkLogic management REST API.
    pass = <PASSWORD>

The 'newrelic' section specifies the New Relic license key as well the name of the component (i.e. name of the cluster on New Relic).
This section is only required when writing stats to New Relic via the ``newrelic`` subcommand.

    [newrelic]
    
    # Your NewRelic license key.
    key = <New Relic Key>
    
    # NewRelic plugin instance name.
    component_name = <NEW RELIC COMPONENT NAME>
    
The 'statsd' section specifies the host and port for the StatsD listener. This section is only required when writing stats to 
a StatsD listener via the ``statsd`` subcommand.


    [statsd]
    
    host = <HOST OF STATSD daemon>
    port = 8125


The 'plugin' section defines sample period for updating your statistics backend, as well as the logging level for emitting messages about plugin operation.

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

Example

    [plugin]
    
    # Local cluster summary.
    summary_status= True
    
    # Database(s) detail status, space delimited
    databases=<DATABASE NAMES>
    
    # Hosts summary, comma delimited
    hosts_summary_status= False
    
    # Host(s) detail status, space delimited
    hosts=<HOST NAMES>
    
    # Forests summary.
    forests_summary_status= False
    
    # Forest(s) detail status, space delimited
    forests=<FOREST NAMES>
    
    # Group(s) detail status, space delimited
    groups=Default
    
    # Servers summary.
    servers_summary_status= False
    
    # Server(s) detail status (must supply group name ex. ServerName:GroupName), space delimited
    servers=<APP SERVER NAMES>
    
The following configurations can also be used to change the sampling rate, add HTTP proxy support if required or change
the debugging level of the output.

    [plugin]
    
    # Proxy (ex. http://10.10.1.10:3128).
    http_proxy =
    
    # Sample period in seconds.
    duration = 60
    
    # Set logging level (INFO|DEBUG|ERROR).
    log_level = DEBUG


Copyright & License
-------------------

AutoPilotCE Copyright 2017 OverStory LLP and is is licensed under the Apache License, Version 2.0 (the "License"),
a copy of the license is included in this [repository](https://github.com/overstory/ml-monitoring-plugin/blob/master/LICENSE).

newrelic-marklogic-plugin Copyright 2017 MarkLogic Corporation 

newrelic-marklogic-plugin is licensed under the Apache License, Version 2.0 (the "License"),
a copy of the license is included in its [repository](https://github.com/marklogic/newrelic-plugin/blob/master/LICENSE).


Acknowledgements
-

Thank you to [MarkLogic Corporation](https://github.com/marklogic) and [Jim Fuller](https://github.com/xquery) for the initial work on the New Relic plugin that inspired this project and
to [SpringerNature](https://github.com/springernature) for providing time to build out the StatsD implementation.