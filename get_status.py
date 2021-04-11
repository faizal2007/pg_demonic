#!/usr/bin/env python

# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import extensions, connect, InterfaceError

# import the psycopg2 errors library
import psycopg2.errors

# import time library
import time

# create a timestamp for the start of the script
start_time = time.time()

# declare a new PostgreSQL connection object
conn = connect(
    dbname = "todo",
    user = "postgres",
    host = "192.168.1.23",
    password = "cyb3rsp@c3"
)

# create a cursor object from the connection
cursor = conn.cursor()

# define a function that parses the connection's poll() response
def check_poll_status():
    """
    extensions.POLL_OK == 0
    extensions.POLL_READ == 1
    extensions.POLL_WRITE == 2
    """

    if conn.poll() == extensions.POLL_OK:
        print ("POLL: POLL_OK")
    if conn.poll() == extensions.POLL_READ:
        print ("POLL: POLL_READ")
    if conn.poll() == extensions.POLL_WRITE:
        print ("POLL: POLL_WRITE")
    return conn.poll()

# define a function that returns the PostgreSQL connection status
def get_transaction_status():

    # print the connection status
    print ("\nconn.status:", conn.status)

    # evaluate the status for the PostgreSQL connection
    if conn.status == extensions.STATUS_READY:
        print ("psycopg2 status #1: Connection is ready for a transaction.")

    elif conn.status == extensions.STATUS_BEGIN:
        print ("psycopg2 status #2: An open transaction is in process.")

    elif conn.status == extensions.STATUS_IN_TRANSACTION:
        print ("psycopg2 status #3: An exception has occured.")
        print ("Use tpc_commit() or tpc_rollback() to end transaction")

    elif conn.status == extensions.STATUS_PREPARED:
        print ("psycopg2 status #4:A transcation is in the 2nd phase of the process.")
    return conn.status

# get transaction status BEFORE
get_transaction_status()

# get the poll status BEFORE
check_poll_status()

try:
    cursor.execute("create table test (id int);")
    cursor.execute("drop table test;")
except Exception as err:

    print ("cursor.execute() ERROR:", err)
    print ("TIME:", time.time() - start_time)

    # get the poll status again
    check_poll_status()

    # get transaction status AFTER
    get_transaction_status()

    # rollback the previous transaction in order to make another
    conn.rollback()

    # make another SQL request to sleep
    cursor.execute("select pg_sleep(4)")

    # get the poll status again
    check_poll_status()

    # get transaction status LAST TIME
    get_transaction_status()


# close the cursor() object to avoid memory leaks
cursor.close()

# close the connection to avoid memory leaks
conn.close()

# polling the connection will now raise an error
try:
    # get the poll one last time
    check_poll_status()
except InterfaceError as error:
    print ("\npsycopg2 ERROR:", error)

# print the elapsed time since the beginning of the script
print ("\nEND TIME:", time.time() - start_time)
