import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Any other environment-specific variables
    DB_CONNECTED = os.getenv('DB_CONNECTED', 'True').lower() in ('true', '1', 't')
    ENV = os.getenv('ENV', 'DEV')
    # Signs login JWTs and email confirm/reset links. Locally a random key is
    # used, so tokens don't survive a restart; deployed envs must set it.
    SECRET_KEY = os.getenv('SECRET_KEY') or (secrets.token_hex(32) if ENV == 'DEV' else None)
    AWS_Key = os.getenv('AWS_Key', "None")
    AWS_Secret = os.getenv('AWS_Secret', "None1")
    AWS_Region = os.getenv('AWS_Region', "None")
    MJ_APIKEY_PRIVATE = os.getenv('MJ_APIKEY_PRIVATE', "None")
    MJ_APIKEY_PUBLIC = os.getenv('MJ_APIKEY_PUBLIC', "None")
    EMAIL_FROM = os.getenv('EMAIL_FROM', "durb.comms@gmail.com")
    # Add more configuration variables as needed

config = Config()