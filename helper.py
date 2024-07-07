from config import prodeventconfigs_collection

for event in prodeventconfigs_collection.find():
    if "repeat" not in event:
        prodeventconfigs_collection.update_one(
            {"_id": event["_id"]}, {"$set": {"repeat": "once"}}
        )
