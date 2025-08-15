'''
Reads a CSV file of sales data then validsates and cleans the data, outputting the clean data to a new CSV file.

'''

import csv
import logging
import re
import sys
import argparse
import os

# Get path to script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one level up and into data/logs
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
LOGS_DIR = os.path.join(BASE_DIR, '..', 'logs')

# ------------------------
# Configuration & Logging
# ------------------------
logging.basicConfig(
    filename= os.path.join(LOGS_DIR, 'errors.log'),
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.WARNING
)

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

# ------------------------
# Data Validation
# ------------------------
def validate_row(row):
    if not row['product'] or row['product'].strip() == '':
        logging.warning(f'{row} - product name is blank')
        return False
    
    try:
        if int(row['quantity']) <= 0:
            logging.warning(f'{row} - quantity is not a positive integer')
            return False
    except ValueError:
        logging.warning(f'{row} - quantity is not a valid integer')
        return False
    except Exception as e:
        logging.warning(f'{row} - unexpected error')
        return False
    
    try:
        if float(row['price']) <= 0:
            logging.warning(f'{row} - price is not a positive float')
            return False
    except ValueError:
        logging.warning(f'{row} - price is not a valid float')
        return False
    except Exception as e:
        logging.warning(f'{row} - unexpected error')
        return False

    if not row['customer_email'] or row['customer_email'].strip() == '' or not EMAIL_REGEX.match(row['customer_email']):
        logging.warning(f'{row} - Invalid email address')
        return False

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
def process_file(input_file, output_file):
    data = read_csv(input_file)
    if data:
        clean_rows = []
        invalid_count = 0
        for row in data:
            if validate_row(row):
                clean_rows.append(transform_row(row))
            else:
                invalid_count += 1

        write_csv(output_file, clean_rows)
        logging.info(f'Processing complete, {len(clean_rows)} valid rows, {invalid_count} invalid rows.')

# ------------------------
# CLI Entrypoint
# ------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and validate sales data.")
    parser.add_argument("input", help="Path to input csv file")
    parser.add_argument("--output", default="clean_data.csv", help="Path to save clean data")
    args = parser.parse_args()

    #ensure data folder exists
    os.makedirs(DATA_DIR, exist_ok=True)

    #create full input/output paths
    input_path = os.path.join(DATA_DIR, args.input)
    output_path = os.path.join(DATA_DIR, args.output)

    process_file(input_path, output_path)
