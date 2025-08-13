import csv
import sqlite3

#------------------
# connect to db
#------------------

conn = sqlite3.connect("../data/sales_data.db")
cur = conn.cursor()

#-----------------
# SQL queries 
#-----------------
column_names = 'transaction_id, product, quantity, customer_email, transaction_date, total_value'
insert_records = f'INSERT INTO sales ({column_names}) VALUES(?, ?, ?, ?, ?, ?)'

select_all = 'SELECT * FROM sales'

#----------------------
# read data in from csv
#----------------------

with open('../data/clean_data.csv') as f:
    data = csv.reader(f)
    cur.executemany(insert_records, data)
    conn.commit()

#---------------------
# check insert
#---------------------
cur.execute(select_all)
print(cur.fetchall())

conn.close()