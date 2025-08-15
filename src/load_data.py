import db_utils
import argparse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, '..', 'config')

if __name__ == '__main__':
    #Connect to DB from config file
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file name.")
    args = parser.parse_args()
    config_path = db_utils.find_config(args.config, CONFIG_DIR)
    
    db, table, columns_and_types, data_file_path = db_utils.load_config(config_path) 
    conn, cur = db_utils.get_connection(db)

    #load data from data file specified in config
    db_utils.insert_records(conn, cur, data_file_path, table, columns_and_types)

    #check insert has worked correctly
    cur.execute(f"SELECT * FROM {table}")
    print(cur.fetchall())
    conn.close()