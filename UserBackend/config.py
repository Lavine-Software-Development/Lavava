import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Any other environment-specific variables
    DB_CONNECTED = os.getenv('DB_CONNECTED', 'True').lower() in ('true', '1', 't')
    ENV = os.getenv('ENV', 'DEV')
    AWS_Key = os.getenv('AWS_Key', "None")
    AWS_Secret = os.getenv('AWS_Secret', "None1")
    AWS_Region = os.getenv('AWS_Region', "None")
    MJ_APIKEY_PRIVATE = os.getenv('MJ_APIKEY_PRIVATE', "None")
    MJ_APIKEY_PUBLIC = os.getenv('MJ_APIKEY_PUBLIC', "None")
    EMAIL_FROM = os.getenv('EMAIL_FROM', "durb.comms@gmail.com")
    # Add more configuration variables as needed
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "None")
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'None')

config = Config()