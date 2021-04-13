#!/usr/bin/env python
import configparser, os, re, click, sys
from pathlib import Path
from pwd import getpwnam
from lib.db import db_connect, check_poll_status
from lib.hot_standby import show_cluster, promote, follow

"""
Initial config file
"""

config_path = Path('/etc/pg_tools/server.conf')
config_path = config_path if config_path.is_file() else Path('config/server.conf')

config = configparser.ConfigParser()
config.read(config_path)

pg_user  = config['general']['pg_user']
pg_uid = getpwnam(pg_user).pw_uid
db = [
        config['server-1']['hostname'], 
        config['server-2']['hostname']
]

#os.setuid(pg_uid)

@click.group()
def cli():
    pass

@click.command()
def show():
    """
    - List all cluster
    """
    show_cluster()

@click.command()
def switch():
    """
    - switch server role
    """
    promote(db)

@click.command()
def rejoin():
    """
    - rejoin new primary
    """
    follow(db)

cli.add_command(show)
cli.add_command(switch)
cli.add_command(rejoin)

if __name__ == '__main__':
    cli()

