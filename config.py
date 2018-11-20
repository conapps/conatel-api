import os
from dotenv import load_dotenv

APP_DIR = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(APP_DIR, '.env')
load_dotenv(dotenv_path)


SQL_URI = os.getenv('POSTGRES_URI')
