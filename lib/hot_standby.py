import re, os, socket
import numpy as np
from subprocess import PIPE, run
from prettytable import PrettyTable

def show_cluster():
    cluster_list = PrettyTable(['Id', 'Node', 'Type', 'Conn'])

    command = ['repmgr', 'cluster', 'show']
    cluster_list = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    if not check_role().stderr:
        print("\nThis node : ", check_role().stdout)
    else:
        print(check_role().stderr)

    print(cluster_list.stdout)


def check_role():
    command = ['repmgr', 'node', 'check', '--role']
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    return result

def promote(db):
    # repmgr standby promote --log-to-file
    # repmgr node rejoin -d "postgres://repmgr@192.168.1.23:5432/repmgr" --force-rewind
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    role = check_role().stdout 
    db =[ d for d in db if d != local_ip].pop(0)

    if re.search('(primary)', role):
        print("Only standby server can be promote \n")
        print("Current role : primary")
        print("Hostname : ", hostname)
        print("Private IP : ", local_ip)
    else:
        if check_db(db).returncode == 0:
            print("db up")
        else:
            command = ['repmgr', 'standby', 'promote', '--log-to-file']
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            print(result.stdout)

def check_db(server):
    command = ['./scripts/check.sh', server]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    return result
