# -*- coding: utf-8 -*-

"""Test bandwidth speed with iperf3"""

from __future__ import print_function  # Python 2

import logging
import os
import re
import subprocess
import sys

__program__ = os.path.basename(os.path.realpath(sys.argv[0]))

# external command dependencies
DEPENDS = ['curl', 'iperf3']


class Speed(object):
    """Test bandwidth speed with iperf3."""

    def __init__(self):
        logging.basicConfig(format='%(levelname)s: %(message)s')

        # ensure dependencies are available
        for dependency in DEPENDS:
            _ensure(dependency)

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

        data = re.match(
            r'{"port":(?P<port>[0-9]+),'
            r'"ip_address":"(?P<ip_address>.*)",'
            r'"scale":true,"protocol":"tcp"}', output).groupdict()

        return data['port'], data['ip_address']

    @property
    def download(self):
        """Determine download speed."""
        return _system(self._command(True) % self._server(), shell=True)

    @property
    def upload(self):
        """Determine upload speed."""
        return _system(self._command() % self._server(), shell=True)


def _ensure(executable, warn=False):
    """Ensure `executable` is installed."""

    try:
        # Python 3.3+ only
        from shutil import which
    except ImportError:

        def which(cmd):
            """
            Given a command, return the path which conforms to the given mode
            on the PATH, or None if there is no such file.
            """

            def _access_check(path):
                """
                Check that a given file can be accessed with the correct mode.
                Additionally check that `path` is not a directory.
                """
                return (os.path.exists(path) and
                        os.access(path, os.F_OK | os.X_OK) and
                        not os.path.isdir(path))

            # If we're given a path with a directory part, look it up directly
            # rather than referring to PATH directories. This includes checking
            # relative to the current directory, e.g. ./script
            if os.path.dirname(cmd):
                if _access_check(cmd):
                    return cmd
                return None

            paths = os.environ.get('PATH', os.defpath.lstrip(':')).split(':')

            seen = set()
            for path in paths:
                if path not in seen:
                    seen.add(path)
                    name = os.path.join(path, cmd)
                    if _access_check(name):
                        return name
            return None

    if which(executable) is None:
        msg = ('%s is not installed', executable)
        if warn:
            logging.warning(*msg)
        else:
            logging.fatal(*msg)
            sys.exit(1)


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
