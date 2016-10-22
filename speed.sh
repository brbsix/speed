#!/bin/bash
#
# Test bandwidth via public iperf3 server

# run iperf3 and print the summarized results
iperf(){
    read -r port address < <(curl -sS --insecure -H 'X-Auth-Key: abc' -H 'X-Auth-Secret: abc' https://104.131.128.139/tcp | awk -F '[:,]' '{gsub("\042", ""); print $2, $4}')
    iperf3 "$@" -p "$port" -c "$address" | awk '/ sender$/ {print $7, $8}'
}

set -euo pipefail

download=$(iperf -R)
echo "Download: $download"

upload=$(iperf)
echo "Upload: $upload"
