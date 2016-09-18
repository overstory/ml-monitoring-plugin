"""MarkLogic Monitoring Plugin bootstrapping."""

# All built-in application controllers should be imported, and registered
# in this file in the same way as MLMonitorBaseController.

from mlmonitor.cli.controllers.base import MLMonitorBaseController

def load(app):
    app.handler.register(MLMonitorBaseController)
