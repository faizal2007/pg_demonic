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
