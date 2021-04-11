#!/bin/bash
CMD="$(dirname $0)/$(basename $0)"

function action() {
    case $1 in
        'create')
            sudo -u postgres createdb $2
        ;;
        'drop')
            sudo -u postgres dropdb $2
        ;;
        *)
            echo "${CMD} <create/drop/list> <db name>"
        ;;
    esac
}

if [ $# -ne 2 ]; then
    echo -e "${CMD} <create/drop/list> <db name>\n"
    echo -e " List of database : "
    sudo -u postgres psql -c "SELECT datname FROM pg_database;" | awk 'NR>2 {print}'
else
    action $1 $2
fi

