from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

prod_client = MongoClient(os.getenv("PROD_DB_URL"))

db = prod_client["test"]
schedules_collection = db["schedules"]
calls_collection = db["calls"]

calls = calls_collection.count_documents({"type": "scheduled"})
schedules = schedules_collection.count_documents({})
successful_schedules = schedules_collection.count_documents({"status": "successful"})
print(f"Total number of schedules: {schedules}")
print(f"Total number of successful schedules: {successful_schedules}")
print(f"Total number of scheduled calls: {calls}")
