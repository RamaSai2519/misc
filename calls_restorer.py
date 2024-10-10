from config import prodcalls_collection, devcalls_collection

prod_calls = list(prodcalls_collection.find({}, {'_id': 0}).sort("_id", -1))
dev_calls = list(devcalls_collection.find({}, {'_id': 0}).sort("_id", -1))

devIds = [call['callId'] for call in dev_calls]

for call in prod_calls:
    if call['callId'] in devIds:
        dev_call = devcalls_collection.find_one({"callId": call['callId']})
        prodcalls_collection.update_one(
            {"callId": call['callId']}, {"$set": dev_call})
        print(f"Restored {call['callId']}")
