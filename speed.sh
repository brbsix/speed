#!/bin/bash
#
# Test bandwidth via public iperf3 server

# run iperf3 and print the summarized results
iperf(){
    iperf3 $1 $(curl -sS --insecure -H 'X-Auth-Key: abc' -H 'X-Auth-Secret: abc' https://104.131.128.139/tcp | awk -F '[:,]' '{gsub("\042", ""); printf "-p %s -c %s", $2, $4}') | awk '/ sender$/ {print $7, $8}'
}

echo "Download: $(iperf -R)"
echo "Upload: $(iperf)"
