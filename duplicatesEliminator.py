from config import prodcalls_collection

calls = list(prodcalls_collection.find())

duplicate_calls = []
seen_calls = set()

for call in calls:
    hours = call['initiatedTime'].hour
    minutes = call['initiatedTime'].minute
    call_key = (call['expert'], call['user'], hours, minutes)
    if call_key in seen_calls and call["status"] == "failed":
        duplicate_calls.append(call)
    else:
        seen_calls.add(call_key)

for call in duplicate_calls:
    print(call["initiatedTime"], call["status"])
    prodcalls_collection.delete_one({"_id": call["_id"]})
