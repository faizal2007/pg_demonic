#!/bin/bash
if [ -f /var/run/postgresql/restart.5432 ]
then
    sleep 5
    /home/freakie/pg_tools/scripts/restart.sh
    rm -f /var/run/postgresql/restart.5432
fi
