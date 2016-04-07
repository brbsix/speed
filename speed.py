# -*- coding: utf-8 -*-

"""Test bandwidth speed with iperf3"""

from __future__ import print_function  # Python 2

# standard imports
import os
import subprocess

# external imports
import yaml


class Speed(object):
    """Test bandwidth speed with iperf3."""

    @staticmethod
    def _command(reverse=False):
        """Craft an appropriate command."""
        return 'iperf3 -p %s -c %s ' + ('-R ' if reverse else '') + \
            "| awk '/ sender$/ {print $7, $8}'"

    @staticmethod
    def _server():
        """Request access to public server, returning port and IP address."""
        output = _system(
            ['curl', '--insecure', '-H',
             'X-Auth-Key: abc', '-H',
             'X-Auth-Secret: abc', 'https://104.131.128.139/tcp']
        )

        # parse output into a YAML document
        data = yaml.load(output)

        return str(data['port']), data['ip_address']

    @property
    def download(self):
        """Determine download speed."""
        return _system(self._command(True) % self._server(), shell=True)

    @property
    def upload(self):
        """Determine upload speed."""
        return _system(self._command() % self._server(), shell=True)


def _system(command, shell=False):
    """Return the output of a command."""
    with open(os.devnull, 'w') as devnull:  # Python 2
        return subprocess.check_output(
            command,
            shell=shell,
            stderr=devnull,
            universal_newlines=True).strip()


def main():
    """Start the application."""
    speed = Speed()
    print('Download: %s' % speed.download)
    print('Upload: %s' % speed.upload)


if __name__ == '__main__':
    main()
