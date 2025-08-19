import csv
import json
import re
import logging
import os
import sys
from datetime import datetime


# resolve file paths
def resolve_path(dir, file_arg):
    if os.path.isabs(file_arg):
        return file_arg
    return os.path.join(dir, file_arg)

# create logging instance
logger = logging.getLogger(__name__)

# Read file schema from json file in config folder
def read_schema(schema_file):
    with open(schema_file) as f:
        try:
            schema = json.load(f)
            return schema
        except json.JSONDecodeError:
            logging.error("Could not read schema.")
            sys.exit(1)

# validate schema
def validate_schema(schema, type_map):
    #schema must contain whether the a value is required for each field and what data type the value must be. 
    #data type must be a valid option from the type_map
    for i in schema:
        if schema[i].get('required') is None or schema[i].get('type') is None:
            logging.error(f'Invalid schema: required / type missing for {i}.')
            print(f'Invalid schema: - required / type missing for {i}.')
            sys.exit(1)
        if schema[i].get('type') not in type_map:
            logging.error(f"Invalid Schema: type for {i} is not valid: {schema[i]['type']}.")
            print(f"Invalid Schema: type for {i} is not valid: {schema[i]['type']}.")
            sys.exit(1)

# check whether required fields are present
def check_required(row, field, schema):
        try:
            if schema[field]['required'] == True:
                if not row[field] or row[field].strip() == '':
                    logging.warning(f'{row} - required field {field} not in row.')
                    return False
        except KeyError:
            logging.warning(f'{row} required not specified in schema for {field}')
            return False
        return True

#Check whether field is the correct type
def check_type(row, field, type):
    value = row[field]
    try:
        type(value)
    except ValueError:
        logging.warning(f'{row} - {field} is incorrect type.')
        return False
    return True

# check whether number meets it's min / max
def valid_number(row, field, schema, type):
        try:
            min_value = schema[field].get('min')
            if min_value is not None and type(row[field]) <= min_value:
                logging.warning(f'{row} - {field} does not exceed it\'s minimum value.')
                return False
        except Exception as e:
            logging.warning(f'{row} - unexpected error')
            return False
        return True

# validate regex
def validate_regex(row, field, regex):
    if not re.match(regex, row[field]):
        return False
    return True

# validate date 
def validate_date(row, field, schema):
    format = schema[field]['format']
    try:
        dt = datetime.strptime(row[field], format)
        row[field] = dt.strftime(format)
    except ValueError:
        logging.warning(f"{row} - invalid {field} format")
        return False
    return True
    
# validate_row
def validate_row(row, schema, type_map):
    for field in schema:
        if not check_required(row, field, schema):
            print(f'{row} check required failed')
            return False
        type = type_map[schema[field].get('type')]
        if type == 'date':
            if not validate_date(row, field, schema):
                print(f"{row} - invalid {field} format")
                return False
        if type != 'date' and not check_type(row, field, type):
            print(f'{row} type check failed')
            return False
        if type == int or type == float:
            if not valid_number(row, field, schema, type):
                print(f'{row} valid_number failed')
                return False
        regex = schema[field].get('regex')
        if regex is not None:
            if not validate_regex(row, field, regex):
                print(f'{row} - Regex check failed')
                return False
    return True

def strip_whitespace(value):
    new_value = value.strip()
    return new_value

def lowercase(value):
    new_value = value.lower()
    return new_value

# func map
func_map = {
    "strip_whitespace" : strip_whitespace,
    "lowercase" : lowercase
}

def transform_row(row, schema, transform_map):
    for field in row:
        for transform in schema[field].get('transform', []):
            func = transform_map[transform]
            row[field] = func(row[field])
    return row

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

def write_csv(output_file, data, schema):
    try:
        with open(output_file, 'w') as f:
            field_names = schema.keys()
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)
    except PermissionError:
        logging.error(f"Permission error, couldn't write to output file.")
        sys.exit(1)

    except Exception as e:
        logging.error(f'Unexpected error {e}')
        sys.exit(1)

def process_file(input_file, output_file, schema, type_map, transform_map):
    data = read_csv(input_file)
    if data:
        clean_rows = []
        invalid_count = 0
        for row in data:
            if validate_row(row, schema, type_map):
                clean_rows.append(transform_row(row, schema, transform_map))
            else:
                invalid_count += 1

        write_csv(output_file, clean_rows, schema)
        logging.info(f'Processing complete, {len(clean_rows)} valid rows, {invalid_count} invalid rows.')

