import logging
import socket

log = logging.getLogger('cement:app:mlmonitor')


class StatsdUtility:
    @staticmethod
    def update_statsd(metric=None, host='localhost', port=8125):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (host, port)

        try:
            # Send data
            log.debug("Sending the following to statsd daemon {0}:{1}: {2}".format(host, port, metric))
            sock.sendto(metric, server_address)

        finally:
            sock.close()
