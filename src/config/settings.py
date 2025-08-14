import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "sponsor_db")
SBER_ID = os.getenv("SBER_ID")
SBER_AUTH = os.getenv("SBER_AUTH")
SBER_SECRET = os.getenv("SBER_SECRET")