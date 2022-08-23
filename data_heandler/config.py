import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_file = os.path.join(os.path.dirname(BASE_DIR), ".env")
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

HOST_NAME = os.getenv('HOST')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
