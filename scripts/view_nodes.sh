sudo -u postgres psql postgres -c 'select node_id, node_name, active,type, config_file from repmgr.nodes' -d repmgr
