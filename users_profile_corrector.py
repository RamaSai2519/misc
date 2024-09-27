from config import produsers_collection as collection

users = list(collection.find())

true_users = 0
false_users = 0

for user in users:
    if "name" in user and "city" in user and "birthDate" in user and user["name"] not in ["", None] and user["city"] not in ["", None] and user["birthDate"] not in ["", None]:
        collection.update_one({"_id": user["_id"]}, {
                              "$set": {"profileCompleted": True}})
        true_users += 1
    else:
        collection.update_one({"_id": user["_id"]}, {
                              "$set": {"profileCompleted": False}})
        false_users += 1

print(f"True users: {true_users}")
print(f"False users: {false_users}")
