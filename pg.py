#!/usr/bin/env python
import configparser, os, re, click
from pathlib import Path
from pwd import getpwnam
from lib.db import db_connect, check_poll_status
from lib.hot_standby import show_cluster

"""
Initial config file
"""
config_path = Path('config/server.conf')

config = configparser.ConfigParser()
config.read(config_path)

pg_user  = config['general']['pg_user']
pg_uid = getpwnam(pg_user).pw_uid
os.setuid(pg_uid)

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
def promote():
    """
    - promote server to primary
    """
cli.add_command(show)
cli.add_command(promote)


if __name__ == '__main__':
    cli()

