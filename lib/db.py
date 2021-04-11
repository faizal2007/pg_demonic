# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import extensions, connect, InterfaceError

# import the psycopg2 errors library
import psycopg2.errors

def db_connect(db, user, host, password):

    conn = connect(
        dbname = db,
        user = user,
        host = host,
        password = password
    )

    return(conn)

# define a function that parses the connection's poll() response
def check_poll_status(conn):
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
