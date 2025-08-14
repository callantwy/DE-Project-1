import db_utils

#--------------
# Config
#--------------

config_path = db_utils.find_config()
db, table, columns_and_types, data_file_path = db_utils.load_config(config_path) 

#------------------
# connect to db
#------------------

conn, cur = db_utils.get_connection(db)

#-----------------
# insert data
#-----------------

db_utils.insert_records(conn, cur, data_file_path, table, columns_and_types)

#---------------------
# check insert
#---------------------

cur.execute(f"SELECT * FROM {table}")
print(cur.fetchall())

conn.close()