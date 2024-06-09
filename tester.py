from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from dotenv import load_dotenv
from pprint import pprint
from time import sleep as s
import os

load_dotenv()

prod_client = MongoClient(os.getenv("PROD_DB_URL"))

db = prod_client["test"]
calls_collection = db["calls"]

doc = os.getenv("DOC")

calls_collection.insert_one(doc)
print("Inserted")

s(5)

calls_collection.delete_one({"callId": "f072938a-8235-48cc-ba09-dca020ccad40"})
print("Deleted")
