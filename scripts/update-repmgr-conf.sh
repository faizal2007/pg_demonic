sudo -u postgres psql postgres -c "update repmgr.nodes set config_file = '/etc/repmgr.conf' where node_id = 2" -d repmgr
