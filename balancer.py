from config import produsers_collection as users_collection, prodcalls_collection as calls_collection

users: list[dict] = list(users_collection.find())

for user in users:
    successful_calls_query = {"status": "successful", "user": user["_id"]}
    calls = calls_collection.count_documents(successful_calls_query)
    if user.get("isPaidUser") is False:
        balance = 3 - calls
        if balance < 0:
            balance = 0
        if user.get("numberOfCalls", 0) != balance:
            users_collection.update_one({"_id": user["_id"]}, {
                                        "$set": {"numberOfCalls": balance}})
            print(f"Updated user {user['_id']} from {user.get('numberOfCalls', 0)} to {balance}")
