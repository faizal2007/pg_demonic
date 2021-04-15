#!/bin/bash
CMD="$(dirname $0)/$(basename $0)"

if [ $# -ne 1 ]; then
    echo "${CMD} <host/ip>"
else
    repmgr -f /etc/repmgr.conf node rejoin -d "postgres://repmgr@${1}:5432/repmgr" --force-rewind
fi

