import sqlite3

conn = sqlite3.connect("../data/sales_data.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS sales (transaction_id int PRIMARY_KEY, product text, quantity int, customer_email text, transaction_date date, total_value real)")

conn.commit()
conn.close()
