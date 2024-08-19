from config import produsers_collection, prodmeta_collection
from bson import ObjectId

users = list(produsers_collection.find())

for user in users:
    user_id = user["_id"]
    if prodmeta_collection.find_one({"user": ObjectId(user_id)}):
        context = prodmeta_collection.find_one({"user": ObjectId(user_id)})
        if "context" not in context:
            context["context"] = ""
        elif "source" not in context:
            context["source"] = ""
        prodmeta_collection.update_one(
            {"user": ObjectId(user_id)}, {"$set": context})
        print(f"Updated context for {user['name']}")
    else:
        prodmeta_collection.insert_one(
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
