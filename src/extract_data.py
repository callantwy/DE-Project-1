'''
Reads a CSV file of sales data then validsates and cleans the data, outputting the clean data to a new CSV file.

'''
import argparse
import os
import data_utils
import logging

# Get path to script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go one level up and into data/logs/config
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
LOGS_DIR = os.path.join(BASE_DIR, '..', 'logs')
SCHEMA_DIR = os.path.join(BASE_DIR, '..', 'config')

#type map used to check types from schema
type_map = {
    "int" : int,
    "str" : str,
    "float" : float,
    "bool" : bool,
    "date" : "date"
}

# ------------------------
# Configuration & Logging
# ------------------------
logging.basicConfig(
    filename= os.path.join(LOGS_DIR, 'errors.log'),
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.WARNING
)

#---------------
# CLI entrypoint
#---------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and validate sales data.")
    parser.add_argument("schema", help="Schema file to define data.")
    parser.add_argument("input", help="Path to input csv file.")
    parser.add_argument("--output", default="clean_data.csv", help="Path to save clean data.")
    args = parser.parse_args()

    #ensure data folder exists
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    #create full input/output paths
    schema_path = data_utils.resolve_path(SCHEMA_DIR, args.schema)
    input_path = data_utils.resolve_path(DATA_DIR, args.input)
    output_path = data_utils.resolve_path(DATA_DIR, args.output)

    schema = data_utils.read_schema(schema_path)
    data_utils.validate_schema(schema, type_map)

    data_utils.process_file(input_path, output_path, schema, type_map, data_utils.func_map)
