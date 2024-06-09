from config import prodcalls_collection, prodcallsmeta_collection

callsmeta = list(prodcallsmeta_collection.find())

for callmeta in callsmeta:
    if "callId" not in callmeta:
        print("callId not found in callmeta")
        continue
    prodcalls_collection.update_one(
        {"callId": callmeta["callId"]},
        {
            "$set": {
                "Conversation Score": callmeta["Conversation Score"],
            }
        },
    )
    print(f"Updated call {callmeta['callId']} with Conversation Score")

print("Done copying Conversation Score to calls collection")
