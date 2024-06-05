from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to the MongoDB client
client = MongoClient(os.getenv("PROD_DB_URL"))
db = client["test"]
meta_collection = db["meta"]
users_collection = db["users"]

users = list(users_collection.find())

for user in users:
    user_id = user["_id"]
    if meta_collection.find_one({"user": ObjectId(user_id)}):
        context = meta_collection.find_one({"user": ObjectId(user_id)})
        if "context" not in context:
            context["context"] = ""
        elif "source" not in context:
            context["source"] = ""
        meta_collection.update_one({"user": ObjectId(user_id)}, {"$set": context})
        print(f"Updated context for {user['name']}")
    else:
        meta_collection.insert_one(
            {
                "user": ObjectId(user_id),
                "context": "",
                "source": "",
            }
        )
        (
            print(f"Inserted empty context for {user['name']}")
            if "name" in user
            else print(f"Inserted empty context for {user['phoneNumber']}")
        )
