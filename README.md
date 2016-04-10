# speed
Test bandwidth via public iperf3 server. There are two scripts, one in Bash, the other in Python. They both do the same thing.

|          |    Interpreter     | Requires |
|----------|:------------------:|:--------:|
| speed.py | Python 2.7 or 3.2+ | requests |
| speed.sh |        Bash        |   curl   |

Example output:

    Download: 567 Kbits/sec
    Upload: 672 Kbits/sec

For information on the server, see: https://github.com/esnet/iperf/issues/380
