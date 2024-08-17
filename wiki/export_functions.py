import pandas as pd
import json
import logging
from .utils import create_data_folder, uuid_to_str

def exportToCsv(df, filename='./data/output.csv'):
    create_data_folder(filename)
    df.to_csv(filename, index=False)
    logging.info(f"Data exported to {filename}")

def exportToJson(df, filename='./data/output.json'):
    create_data_folder(filename)
    # Convert DataFrame to dict, handling UUID conversion
    json_data = df.to_dict(orient='records')
    json_data = [{k: uuid_to_str(v) for k, v in record.items()} for record in json_data]
    
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=2)
    logging.info(f"Data exported to {filename}")
