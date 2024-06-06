from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to the MongoDB client
dev_client = MongoClient(os.getenv("DEV_DB_URL"))
db = dev_client["test"]
meta_collection = db["meta"]


# Function to find all unique keys in a collection
def find_unique_keys(collection):
    unique_keys = set()
    cursor = collection.find()
    for document in cursor:
        unique_keys.update(document.keys())
    return unique_keys


# Example usage
unique_keys = find_unique_keys(meta_collection)
print("Unique keys in the collection:")
for key in unique_keys:
    print(key)
