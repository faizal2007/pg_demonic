SQL="select * from pg_user;"
#echo $SQL
sudo -u postgres psql -c "$SQL" -d postgres
