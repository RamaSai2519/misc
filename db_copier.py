from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

prod_client = MongoClient(os.getenv("PROD_DB_URL"))
dev_client = MongoClient(os.getenv("DEV_DB_URL"))
prod_db = prod_client["test"]
dev_db = dev_client["test"]

prod_collections = list(prod_db.list_collection_names())

for collection_name in prod_collections:
    if collection_name == "schedules":
        prod_collection = prod_db.get_collection(collection_name)
        dev_collection = dev_db.get_collection(collection_name)
        dev_collection.drop()
        print(f"Copying {collection_name} from prod to dev")
        documents = list(prod_collection.find())
        for document in documents:
            dev_collection.insert_one(document)
