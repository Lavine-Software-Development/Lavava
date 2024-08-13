import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Any other environment-specific variables
    USER_BACKEND_URL = os.getenv('USER_BACKEND_URL', 'https://userbackend.durb.ca:5001')
    USER_BACKEND_LOCAL_URL = os.getenv('USER_BACKEND_LOCAL_URL', 'http://userbackend:5001')
    USER_BACKEND_STAGING_URL = os.getenv('USER_BACKEND_STAGING_URL', 'https://userbackend.durb.ca:5002')
    ENV = os.getenv('ENV', 'DEV')

    # Add more configuration variables as needed

config = Config()