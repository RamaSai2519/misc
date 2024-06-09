from config import produsers_collection, prodexperts_collection

for user in list(produsers_collection.find({"isBusy": True})):
    user["isBusy"] = False
    produsers_collection.update_one({"_id": user["_id"]}, {"$set": user})
    print(f"Set isBusy to False for user {user['name']}")
    for expert in list(prodexperts_collection.find({"isBusy": True})):
        expert["isBusy"] = False
        prodexperts_collection.update_one({"_id": expert["_id"]}, {"$set": expert})
        print(f"Set isBusy to False for expert {expert['name']}")
