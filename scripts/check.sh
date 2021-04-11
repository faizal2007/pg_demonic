#!/bin/bash
CMD="$(dirname $0)/$(basename $0)"

if [ $# -ne 1 ]; then
    echo "${CMD} <host/ip>"
else
    sudo -u postgres pg_isready -h $1 -p 5432
fi

