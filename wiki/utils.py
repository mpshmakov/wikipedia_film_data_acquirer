import os
import uuid
import logging

def create_data_folder(filename):
    data_dir = os.path.dirname(filename)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logging.info(f"Created directory: {data_dir}")

def uuid_to_str(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    return obj

def clean_numeric(value):
    if isinstance(value, str):
        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
            return int(float(value))
    return value
