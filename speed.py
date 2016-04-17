#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Test bandwidth via public iperf3 server"""

from __future__ import print_function, unicode_literals  # Python 2

import errno
import logging
import os
import subprocess
import sys

import requests

__program__ = os.path.basename(os.path.realpath(sys.argv[0]))


class Speed(object):
    """Test bandwidth speed with iperf3."""

    def __init__(self):
        logging.basicConfig(format='%(levelname)s: %(message)s')

        # disable urllib3's InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning)

    def _iperf(self, reverse=False):
        """Run iperf3 with the appropriate arguments then parse the output."""
        server = self._server()

        try:
            command = ['iperf3', '-p', '%d' % server['port'], '-c',
                       server['ip_address']] + (['-R'] if reverse else [])
        except KeyError:
            logging.error(server['error'])
            sys.exit(1)

        with open(os.devnull, 'w') as devnull:  # Python 2 and 3.2
            try:
                # run the command and store the output
                output = subprocess.check_output(
                    command,
                    stderr=devnull,
                    universal_newlines=True)
            except OSError as exc:
                if exc.errno == errno.ENOENT:
                    logging.error('iperf3 is not installed')
                    sys.exit(1)
                raise

        # extract the speed from iperf output
        for line in output.splitlines():
            if line.endswith(' sender'):
                return ' '.join(line.split()[6:8])

    @staticmethod
    def _server():
        """Request access to public server, returning port and IP address."""
        url = 'https://104.131.128.139/tcp'
        headers = {'X-Auth-Key': 'abc', 'X-Auth-Secret': 'abc'}

        try:
            return requests.get(url, headers=headers, verify=False).json()
        except requests.exceptions.ConnectionError:
            logging.error('server is unreachable')
            sys.exit(1)

    @property
    def download(self):
        """Determine download speed."""
        return self._iperf(reverse=True)

    @property
    def upload(self):
        """Determine upload speed."""
        return self._iperf()


def main():
    """Start the application."""
    speed = Speed()
    print('Download: %s' % speed.download)
    print('Upload: %s' % speed.upload)


if __name__ == '__main__':
    main()
