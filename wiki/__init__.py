# Standard library imports
import os
import uuid
import json
import logging

# Third-party imports
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Local imports
from .utils import create_data_folder, uuid_to_str
from .export_functions import exportToCsv, exportToJson

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetchPage(url):
    try:
        res = requests.get(url)
        logging.info("Successfully fetched the page")
        return res
    except:
        logging.error("Failed to fetch the page - No internet connection.")
        raise Exception("Failed to fetch the page - No internet connection.")

# Expose commonly used functions and classes
__all__ = [
    'pd',
    'BeautifulSoup',
    'requests',
    'logging',
    'uuid',
    'exportToCsv',
    'exportToJson',
    'create_data_folder',
    'uuid_to_str',
    'fetchPage'
]