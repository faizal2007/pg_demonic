#!/bin/bash
CMD="$(dirname $0)/$(basename $0)"

if [ $# -ne 1 ]; then
    echo "${CMD} <host/ip>"
else
    pg_isready -h $1 -p 5432
fi

