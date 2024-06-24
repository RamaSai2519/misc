from config import prodschedules_collection

schedules = list(prodschedules_collection.find({}, {"_id": 1}))

for schedule in schedules:
    prodschedules_collection.update_one(
        {"_id": schedule["_id"]}, {"$set": {"type": "Admin"}}
    )
