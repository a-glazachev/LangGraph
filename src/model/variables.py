"""
Module: model/variables.py
Description:
    This module is responsible for loading and managing environment variables.
    It uses the dotenv library to load variables from a .env file,
    making it easier to manage sensitive information.
"""

import os

from dotenv import load_dotenv

load_dotenv()

YC_API_KEY = os.getenv("YC_API_KEY")
YC_FOLDER_ID = os.getenv("YC_FOLDER_ID")
