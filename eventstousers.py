from config import prodevents_collection, produsers_collection

event_users = list(prodevents_collection.find(
    {"phoneNumber": {"$exists": True}, "dob": {"$exists": True},
        "city": {"$exists": True}, "name": {"$exists": True}, "createdAt": {"$exists": True}}
))

for user in event_users:
    if produsers_collection.find_one({"phoneNumber": user["phoneNumber"]}):
        print(f"User {user['name']} already exists")
    else:
        fuser = produsers_collection.insert_one({
            "phoneNumber": user["phoneNumber"],
            "otp": "",
            "expiresOtp": "",
            "isBusy": False,
            "active": True,
            "createdDate": user["createdAt"],
            "numberOfCalls": 3,
            "profileCompleted": True,
            "birthDate": user["dob"],
            "city": user["city"],
            "name": user["name"]
        })
        new_id = fuser.inserted_id
        prodevents_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"user_id": new_id}}
        )
        print(f"User {user['name']} added to produsers_collection")
print("All users added")
