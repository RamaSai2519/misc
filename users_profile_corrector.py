from config import produsers_collection as collection

users = list(collection.find())

true_users = []
false_users = []

for user in users:
    if "name" in user and "birthDate" in user and user["name"] not in ["", None] and user["birthDate"] not in ["", None]:
        true_users.append(user["_id"])
    else:
        false_users.append(user["_id"])

true_update = collection.update_many({"_id": {"$in": true_users}}, {"$set": {"profileCompleted": True}})
false_update = collection.update_many({"_id": {"$in": false_users}}, {"$set": {"profileCompleted": False}})

print(f"Updated {true_update.modified_count} users with profileCompleted: True")
print(f"Updated {false_update.modified_count} users with profileCompleted: False")

print(f"True users: {len(true_users)}")
print(f"False users: {len(false_users)}")
