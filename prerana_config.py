from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MARKERS_DB_URL"))

prerana_db = client["prerana"]

prusers_collection = prerana_db["users"]
