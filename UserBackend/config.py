# config.py

import os

class Config:
    # Any other environment-specific variables
    DB_CONNECTED = os.getenv('DB_CONNECTED', 'True').lower() in ('true', '1', 't')

    # Add more configuration variables as needed

config = Config()