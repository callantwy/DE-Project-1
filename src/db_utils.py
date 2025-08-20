import sqlite3
import csv
import json 
import os
import logging
import sys
import datetime

# create logging instance
logger = logging.getLogger(__name__)

# db config utils
def find_config(config_name, CONFIG_DIR):
    config_path = os.path.join(CONFIG_DIR, config_name)
    return config_path

def load_config(config_file_path):
    try:
        with open(config_file_path) as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError as e:
                logging.error(f"Can't parse {config_file_path}")
                print("Invalid config file - can't parse.")
                sys.exit(1)
    except FileNotFoundError:
        logging.error(f"{config_file_path} not found")
        print("Config file not found.")
        sys.exit(1)
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

# reporting
def read_report_config(report_config_file):
    try:
        with open(report_config_file) as f:
            try:
                report_config = json.load(f)
            except json.JSONDecodeError:
                logging.error(f"Can't parse {report_config}")
                print("Invalid schema - can't parse")
    except FileNotFoundError:
        print("Schema file not found.")
        logging.error(f'{report_config_file} not found.')
        sys.exit(1)
    return report_config

def replace_date(output_file):
    today = datetime.date.today()
    formatted = today.strftime('%Y%m%d')
    output_file = output_file.replace('{date}', formatted)
    return output_file

def write_report(cur, config):
    for report in config:
        try:
            cur.execute(report['query'])
        except sqlite3.OperationalError:
            logging.warning("OperationalError - invalid query in")
        headers = [col[0] for col in cur.description]
        output_file = replace_date(report['output_file'])
        with open(f'{output_file}', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(cur.fetchall())
