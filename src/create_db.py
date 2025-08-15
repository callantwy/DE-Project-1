import db_utils
import argparse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, '..', 'config')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file name.")
    args = parser.parse_args()
    config_path = db_utils.find_config(args.config, CONFIG_DIR)
    
    #create database and table
    db, table, columns_and_types, data_file_path = db_utils.load_config(config_path) 
    conn, cur = db_utils.get_connection(db)
    db_utils.create_table(conn, cur, table, columns_and_types)
    conn.close()

