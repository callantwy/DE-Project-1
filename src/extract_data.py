'''
Reads a CSV file of sales data then validsates and cleans the data, outputting the clean data to a new CSV file.

'''

import csv
import logging
import re
import sys

# ------------------------
# Configuration & Logging
# ------------------------
logging.basicConfig(
    filename="error.log",
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

# ------------------------
# Data Validation
# ------------------------
def validate_row(row):
    if not row['product'] or row['product'].strip() == '':
        return False
        logging.error(f'{row} - product name is blank')
    
    try:
        if int(row['quantity']) <= 0:
            return False
            logging.error(f'{row} - quantity is not a positive integer')
    except ValueError:
        return False
        logging.error(f'{row} - quantity is not a valid integer')
    except Exception as e:
        return False
        logging.error(f'{row} - unexpected error')

    try:
        if float(row['price']) <= 0:
            return False
            logging.error(f'{row} - price is not a positive float')
    except ValueError:
        return False
        logging.error(f'{row} - price is not a valid float')
    except Exception as e:
        return False
        logging.error(f'{row} - unexpected error')

    if not row['customer_email'] or row['customer_email'].strip() == '' or not EMAIL_REGEX.match(row['customer_email']):
        return False
        logging.error(f'{row} - Invalid email address')

    return True
# ------------------------
# Transformation Functions
# ------------------------
def transform_row(row):
    row['product'] = row['product'].strip()
    row['customer_email'] = row['customer_email'].strip()
    row['transaction_date'] = row['transaction_date'].replace('/','-')
    row['transaction_date'] = row['transaction_date'].replace('.','-')
    return row
# ------------------------
# I/O Functions
# ------------------------
def read_csv(filename):
    try:
        with open(filename) as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        sys.exit(1)
    except PermissionError:
        logging.error(f"Permission denied reading {file_path}")
        sys.exit(1)

def write_csv(output_file, data):
    try:
        with open(output_file, 'w') as f:
            field_names = ['transaction_id', 'product', 'quantity', 'price', 'customer_email', 'transaction_date']
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)
    except PermissionError:
        logging.error(f"Permission error, couldn't write to output file.")
        sys.exit(1)

    except Exception as e:
        logging.error(f'Unexpected error {e}')
        sys.exit(1)

# ------------------------
# Main Processing
# ------------------------
if __name__ == '__main__':
    input_file = 'data.csv'
    output_file = 'clean_data.csv'

    data = read_csv(input_file)
    if data:
        clean_data = []
        for row in data:
            if validate_row(row):
                clean_data.append(transform_row(row))
        write_csv(output_file, clean_data)

# ------------------------
# CLI Entrypoint
# ------------------------

