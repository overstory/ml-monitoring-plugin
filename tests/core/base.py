import logging
from threading import Thread
from unittest import TestCase

from bottle import Bottle

log = logging.getLogger('cement:app:mlmonitor')
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
log.setLevel(logging.DEBUG)


class ServeredTestCase(TestCase):
    app = Bottle()
    t = Thread()

    def setUp(self):
        self.t = Thread(target=self.app.run, args=())
        self.t.setDaemon(True)
        self.t.start()
