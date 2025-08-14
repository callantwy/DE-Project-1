import db_utils

if __name__ == "__main__":
    
    config_path = db_utils.find_config()
    
    #create database and table
    db, table, columns_and_types, data_file_path = db_utils.load_config(config_path) 
    conn, cur = db_utils.get_connection(db)
    db_utils.create_table(conn, cur, table, columns_and_types)
    conn.close()

