"""
Wiki module initialization.

This module sets up logging and imports necessary components for web scraping
and data processing operations.
"""

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
    """
    Fetch a web page and return the response.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        requests.Response: The response object from the request.

    Raises:
        Exception: If the page cannot be fetched due to network issues.
    """
    try:
        res = requests.get(url)
        logging.info("Successfully fetched the page")
        return res
    except requests.RequestException:
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
