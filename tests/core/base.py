import logging
from threading import Thread

log = logging.getLogger('cement:app:mlmonitor')
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
log.setLevel(logging.DEBUG)


def requires_http_server(app, host, port):
    def outer_wrapper(f):
        def wrapper(*args, **kwargs):
            t = Thread(target=app.run, kwargs={'host': host, 'port': port, 'debug': True})
            t.setDaemon(True)
            t.start()

            return f(*args, **kwargs)

        return wrapper

    return outer_wrapper
