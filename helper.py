from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("PROD_DB_URL"))
db = client["test"]
users_collection = db["users"]
experts_collection = db["experts"]

for user in list(users_collection.find({"isBusy": True})):
    user["isBusy"] = False
    users_collection.update_one({"_id": user["_id"]}, {"$set": user})
    print(f"Set isBusy to False for user {user['name']}")
    for expert in list(experts_collection.find({"isBusy": True})):
        expert["isBusy"] = False
        experts_collection.update_one({"_id": expert["_id"]}, {"$set": expert})
        print(f"Set isBusy to False for expert {expert['name']}")
