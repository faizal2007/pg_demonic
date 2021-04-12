#!/bin/bash
PID=$((`ps aux | grep "postgres -D" | grep -v grep | awk '{print $2}'`))

if [ -f /var/run/postgresql/11-main.pid ]
then
    echo "postgres stoping..."
    /usr/bin/pg_ctlcluster 11 main stop
    echo "postgres stopped."
fi

if [ ! -f /var/run/postgresql/11-main.pid ] &&  [ $PID -eq 0 ]
then
    kill -9 $PID
fi

if [ ! -f /var/run/postgresql/11-main.pid ]
then
    echo "postgres starting..."
    /usr/bin/pg_ctlcluster 11 main start
    echo "postgres started."
fi
