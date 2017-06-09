"""MarkLogic Monitoring Plugin main application entry point."""
import platform

from cement.core.exc import FrameworkError, CaughtSignal
from cement.core.foundation import CementApp
from cement.ext.ext_logging import LoggingLogHandler
from cement.utils.misc import init_defaults

from mlmonitor.core import exc

# Application default.  Should update config/mlmonitor.conf to reflect any
# changes, or additions here.
defaults = init_defaults('mlmonitor')

# All internal/external plugin configurations are loaded from here
defaults['mlmonitor']['plugin_config_dir'] = '/etc/mlmonitor/plugins.d'

# External plugins (generally, do not ship with application code)
defaults['mlmonitor']['plugin_dir'] = '/var/lib/mlmonitor/plugins'

# External templates (generally, do not ship with application code)
defaults['mlmonitor']['template_dir'] = '/var/lib/mlmonitor/templates'


# This custom log handler is to bypass problems with the default cement logger
class CustomLogHandler(LoggingLogHandler):
    class Meta:
        label = 'mlmonitor_logger'

        #: The logging format for the file logger.
        file_format = "%(asctime)s (%(levelname)s) : %(message)s"

        #: The logging format for the consoler logger.
        console_format = "%(levelname)s: %(message)s"

        #: The logging format for both file and console if ``debug==True``.
        debug_format = "%(asctime)s (%(levelname)s) : %(message)s"


def reload_commandline_config(app):
    if (app.pargs.config):
        app.config.parse_file(app.pargs.config)
    # Daemonize here.  Need to be able to get location of pid file after command line config has been loaded
    if not platform.system().lower() in ['windows']:
        app.daemonize()


class MLMonitorApp(CementApp):
    class Meta:
        label = 'mlmonitor'
        config_defaults = defaults
        config_files = [
            '~/.mlmonitor/application.conf',
            '../../config/mlmonitor.conf'
        ]
        if not platform.system().lower() in ['windows']:
            extensions = ['daemon']
        log_handler = 'mlmonitor_logger'
        handlers = [
            CustomLogHandler
        ]

        hooks = [
            ('post_argument_parsing', reload_commandline_config)
        ]

        # All built-in application bootstrapping (always run)
        bootstrap = 'mlmonitor.cli.bootstrap'

        # Internal plugins (ship with application code)
        plugin_bootstrap = 'mlmonitor.cli.plugins'

        # Internal templates (ship with application code)
        template_module = 'mlmonitor.cli.templates'

        # call sys.exit() when app.close() is called
        exit_on_close = True


class MLMonitorTestApp(MLMonitorApp):
    """A test app that is better suited for testing."""

    class Meta:
        # default argv to empty (don't use sys.argv)
        argv = []

        # don't look for config files (could break tests)
        config_files = []

        # don't call sys.exit() when app.close() is called in tests
        exit_on_close = False


# Define the applicaiton object outside of main, as some libraries might wish
# to import it as a global (rather than passing it into another class/func)
app = MLMonitorApp()


def main():
    with app:
        try:
            app.args.add_argument('-c', action='store', dest='config', help='Location of config file to parse')
            app.run()

        except exc.MLMonitorError as e:
            # Catch our application errors and exit 1 (error)
            print('MLMonitorError > %s' % e)
            app.exit_code = 1

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            from signal import SIGINT, SIGABRT

            if e.signum == SIGINT:
                app.exit_code = 110
            elif e.signum == SIGABRT:
                app.exit_code = 111

        except FrameworkError as e:
            # Catch framework errors and exit 1 (error)
            print('FrameworkError > %s' % e)
            app.exit_code = 300

        finally:
            # Maybe we want to see a full-stack trace for the above
            # exceptions, but only if --debug was passed?
            if app.debug:
                import traceback
                traceback.print_exc()


if __name__ == '__main__':
    main()
