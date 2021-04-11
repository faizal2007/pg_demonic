#!/bin/bash
PID=$((`ps aux | grep "postgres -D" | grep -v grep | awk '{print $2}'`))

if [ -f /var/run/postgresql/11-main.pid ]
then
    /usr/bin/pg_ctlcluster 11 main stop
fi

if [ ! -f /var/run/postgresql/11-main.pid ] &&  [ $PID -gt 0 ]
then
    kill -9 $PID
fi

if [ ! -f /var/run/postgresql/11-main.pid ]
then
    /usr/bin/pg_ctlcluster 11 main start
fi
