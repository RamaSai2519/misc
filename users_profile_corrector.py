from shared.db.users import get_user_collection

collection = get_user_collection()
users = list(collection.find())

true_users = []
false_users = []

for user in users:
    fields = ["name", "birthDate", "city"]
    if all(field in user and user[field] not in ["", None] for field in fields):
        true_users.append(user["_id"])
    else:
        false_users.append(user["_id"])

true_update = collection.update_many({"_id": {"$in": true_users}}, {
                                     "$set": {"profileCompleted": True}})
false_update = collection.update_many({"_id": {"$in": false_users}}, {
                                      "$set": {"profileCompleted": False}})

print(f"Updated {true_update.modified_count} users with profileCompleted: True")
print(
    f"Updated {false_update.modified_count} users with profileCompleted: False")

print(f"True users: {len(true_users)}")
print(f"False users: {len(false_users)}")
