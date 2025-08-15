import sqlite3
import csv
import json 
import argparse
import os

def find_config(config_name, CONFIG_DIR):
    config_path = os.path.join(CONFIG_DIR, config_name)
    return config_path

def load_config(config_file_path):
    with open(config_file_path) as f:
        config = json.load(f)
    db = config['db']
    table = config['table']
    columns_and_types = config['types']
    data_file_path = config['data_file_path']
    return db, table, columns_and_types, data_file_path

def get_column_names(column_names_types):
    column_names = ", ".join(column_names_types.keys())
    return column_names

def get_connection(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    return conn, cur

# how do we enforce that column_names_types is dict

def create_table(conn, cur, table_name, column_names_types):
    column_names = get_column_names(column_names_types)
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({column_names})')
    conn.commit()

def insert_records(conn, cur, file_path, table, column_names_types):
    column_names = get_column_names(column_names_types)
    placeholders = ", ".join(['?'] * len(column_names_types))
    insert_records = f'INSERT INTO {table} ({column_names}) VALUES({placeholders})'
    with open(file_path) as f:
        data = csv.reader(f)
        next(f)
        cur.executemany(insert_records, data)
        conn.commit()

def write_report(cur, query, file_name):
    cur.execute(query)
    headers = [col[0] for col in cur.description]
    with open('../reports/'+file_name+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(cur.fetchall())
