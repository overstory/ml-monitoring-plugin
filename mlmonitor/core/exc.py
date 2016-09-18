"""MarkLogic Monitoring Plugin exception classes."""

class MLMonitorError(Exception):
    """Generic errors."""
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg

class MLMonitorConfigError(MLMonitorError):
    """Config related errors."""
    pass

class MLMonitorRuntimeError(MLMonitorError):
    """Generic runtime errors."""
    pass

class MLMonitorArgumentError(MLMonitorError):
    """Argument related errors."""
    pass
