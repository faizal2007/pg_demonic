import re, os, socket, sys, time
from subprocess import PIPE, run
from prettytable import PrettyTable
from pathlib import Path

root = "/home/freakie/pg_tools"

def show_cluster():
    #cluster_list = PrettyTable(['Id', 'Node', 'Type', 'Conn'])

    command = ['repmgr', 'cluster', 'show']
    cluster_list = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    if not check_role().stderr:
        print("\nStatus : ", check_role().stdout)
    else:
        print(check_role().stderr)

    print(cluster_list.stdout)


def check_role():
    command = ['repmgr', 'node', 'check', '--role']
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    return result

def promote(db):
    get_ip()

    role = check_role().stdout 
    db =[ d for d in db if d != local].pop(0)

    if re.search('(primary)', role):
        print("Only standby server can be promote \n")
        print("Current role : primary")
        print("Hostname : ", hostname)
        print("Private IP : ", local)
    else:
        if check_db(db).returncode == 0:
            command = ['repmgr', 'standby', '-f', '/etc/repmgr.conf', 'switchover', '--log-to-file']

            print("waiting for server to promote...")
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            print(result.stderr if result.returncode > 0 else "server promoted.")
        else:
            command = ['repmgr', 'standby', '-f', '/etc/repmgr.conf','promote', '--log-to-file']

            print("waiting for server to promote...")
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            print("server promoted." if result.returncode == 0 else "server promotion failed.")
            time.sleep(5)
            print(follow(db, remote=True))

def check_db(server):
    script = root + "/scripts/check.sh"
    command = [script, server]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    return result

def touch(db, trigger):
    command = ['ssh', db, 'touch /var/run/postgresql/' + trigger]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    return result.returncode

def follow(db, remote = False):
    get_ip()
    db_status = check_db(local)
    #print(db_status.returncode)

    next =[ d for d in db if d != local].pop(0)

    role = check_role().stdout
    if remote:
        command = ['ssh', db, '/usr/local/bin/pg rejoin']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return result.stdout
    else:
        if re.search('(primary)', role):
            print("This feature only works for standby role \n")
            print("Current role : primary")
            print("Hostname : ", hostname)
            print("Private IP : ", local)
        else:
            if db_status.returncode != 0:
                script = root + "/scripts/rejoin.sh"
                command = [script, next]
                result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                print(result.stderr)
            else:
                print("\nNode status :" + role)

def get_ip(type='private'):
    global local, public, hostname

    if type == 'private':
        hostname = socket.gethostname()
        local = socket.gethostbyname(hostname)

