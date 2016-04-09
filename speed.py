# -*- coding: utf-8 -*-

"""Test bandwidth speed with iperf3"""

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

    @staticmethod
    def _iperf(port, ip_address, reverse=False):
        """Run iperf3 with the appropriate arguments then parse the output."""
        command = ['iperf3', '-p', port, '-c', ip_address] + \
            (['-R'] if reverse else [])

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

        # disable urllib3's InsecureRequestWarning
        urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning)
        output = requests.get(url, headers=headers, verify=False).text

        pattern = r'{"port":(?P<port>[0-9]+),"ip_address":"' \
                  r'(?P<ip_address>.*)","scale":true,"protocol":"tcp"}'

        data = re.match(pattern, output).groupdict()

        return data['port'], data['ip_address']

    @property
    def download(self):
        """Determine download speed."""
        return self._iperf(*self._server(), reverse=True)

    @property
    def upload(self):
        """Determine upload speed."""
        return self._iperf(*self._server())


def main():
    """Start the application."""
    speed = Speed()
    print('Download: %s' % speed.download)
    print('Upload: %s' % speed.upload)


if __name__ == '__main__':
    main()
