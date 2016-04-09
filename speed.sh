#!/bin/bash
#
# Test bandwidth via public iperf3 server

# run iperf3 and print the parsed output
iperf(){
    local fields ip_address output port reverse

    # use -R flag for download
    [[ $1 = --reverse ]] && reverse='-R'

    # extract server info from YAML response
    output=$(request)
    fields=$(echo "$output" | sed 's/}$//;s/,/\n/g' | sed 's/^.*://;s/"//g')
    port=$(echo "$fields" | sed -n 1p)
    ip_address=$(echo "$fields" | sed -n 2p)

    # run iperf and only print the summarized result
    iperf3 $reverse -p "$port" -c "$ip_address" | awk '/ sender$/ {print $7, $8}'
}

# use credentials to request access from server
request(){
    curl -s --insecure -H 'X-Auth-Key: abc' -H 'X-Auth-Secret: abc' https://104.131.128.139/tcp
}

echo "Download: $(iperf --reverse)"
echo "Upload: $(iperf)"
