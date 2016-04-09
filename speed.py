#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Test bandwidth via public iperf3 server"""

from __future__ import print_function  # Python 2

import errno
import logging
import os
import re
import subprocess
import sys

import requests
import urllib3

__program__ = os.path.basename(os.path.realpath(sys.argv[0]))


class Speed(object):
    """Test bandwidth speed with iperf3."""

    def __init__(self):
        logging.basicConfig(format='%(levelname)s: %(message)s')

        # disable urllib3's InsecureRequestWarning
        urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning)

    def _iperf(self, reverse=False):
        """Run iperf3 with the appropriate arguments then parse the output."""
        server = self._server()

        command = ['iperf3', '-p', server['port'], '-c', server['ip_address']
                   ] + (['-R'] if reverse else [])

        with open(os.devnull, 'w') as devnull:  # Python 2
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

        output = requests.get(url, headers=headers, verify=False).text

        pattern = r'{"port":(?P<port>[0-9]+)' \
                  r',"ip_address":"(?P<ip_address>.*)"' \
                  r',"scale":(?P<scale>false|true)' \
                  r',"protocol":"(?P<protocol>tcp|udp)"}'

        return re.match(pattern, output).groupdict()

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
