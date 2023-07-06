from os import path, getenv
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(path.join(BASE_DIR, ".env"))
SECRET_KEY = getenv("SECRET_KEY")

channel = getenv("CHANNEL")
DEBUG = getenv("DEBUG", "False") == "True"
PREFIX_KEY = getenv('PREFIX_KEY')

DB_USERNAME = getenv("DB_USER")
DB_NAME = getenv("DB_NAME")
DB_PASSWORD = getenv("DB_PASSWORD")

EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_HOST_USER = getenv("EMAIL_USER")
EMAIL_HOST_PASSWORD = getenv("EMAIL_PASSWORD")
EMAIL_PORT = getenv("EMAIL_PORT")
