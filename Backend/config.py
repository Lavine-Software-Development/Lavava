import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Any other environment-specific variables
    USER_BACKEND_URL = os.getenv('USER_BACKEND_URL', 'https://userbackend.durb.ca:5001')

    # Add more configuration variables as needed

config = Config()