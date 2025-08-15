import db_utils 
import csv
import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, '..', 'config')

# Total sales value for each product.
queries = {"total_sales":"SELECT product, sum(quantity * price) as total_spend FROM sales GROUP BY product;",
"transactions_per_day":"SELECT transaction_date, COUNT(DISTINCT transaction_id) as num_transactions FROM sales GROUP BY transaction_date;",
"top_customers":"SELECT customer_email, count(*) as num_purchases FROM sales GROUP BY customer_email ORDER BY num_purchases DESC LIMIT 3;",
"average_order_value":"SELECT ROUND(AVG(quantity * price), 2) as average_order FROM sales;"}

if __name__ == '__main__':
    #Build parser which takes config file and an SQL query as arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='Specify the config file that has the details of your db')
    parser.add_argument('query', help='Specify the SQL query you would like to run. Options are total_sales, transactions_per_day, top_customers or average_order_value or all')
    args = parser.parse_args()

    #Connect to DB
    config_path = db_utils.find_config(args.config, CONFIG_DIR)
    db, table, columns_and_types, data_file_path = db_utils.load_config(config_path) 
    conn, cur = db_utils.get_connection(db)

    #Write report to csv
    if args.query == 'all':
        for query_name, query in queries.items():
            file_name = query_name
            db_utils.write_report(cur, query, file_name)
    else:
        try:
            query = queries[args.query]
        except KeyError:
            print("Query not found. Please see --help for list of queries.")
            sys.exit(1)
        file_name = args.query
        db_utils.write_report(cur, query, file_name)
        
