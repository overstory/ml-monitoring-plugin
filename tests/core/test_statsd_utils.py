import socket
from threading import Thread
from unittest import TestCase

import logging

from mlmonitor.core.utils.statsd_utils import StatsdUtility

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class StatsdUtilsTests(TestCase):
    host = '127.0.0.1'
    port = 10000

    message = None

    def setUp(self):
        def udp_run():
            log.debug('UDP server starting up at {0}:{1}'.format(self.host, self.port))
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = (self.host, self.port)
            sock.bind(server_address)

            while 1:
                data, address = sock.recvfrom(4096)
                self.message = data
                log.debug("UDP server received the message: " + self.message)

        self.t = Thread(target=udp_run, args=())
        self.t.setDaemon(True)
        self.t.start()

    def test_statsd_util(self):
        test_message = 'Test message here'
        StatsdUtility.update_statsd(test_message, self.host, self.port)

        self.assertEquals(self.message, test_message)

    def tearDown(self):
        return
