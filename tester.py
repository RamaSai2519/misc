from config import prodcalls_collection
from time import sleep as s
from bson import ObjectId
import datetime

experts = [
    ObjectId("66046a3d42f04a057fa21034"),
    ObjectId("6604694542f04a057fa2100f")
]

i = 0

while True:
    i += 1
    if i == 10:
        break
    document = {
        "callId": "f072938a-8235-48cc-ba09-dca020ccad40",
        "duration": "0:1:32",
        "expert": experts[0],
        "failedReason": "",
        "initiatedTime": datetime.datetime(2024, 6, 13, 14, 20, 20, 988000),
        "recording_url": "https://sr.knowlarity.com/vr/fetchsound/?callid%3Df072938a-8235-48cc-ba09-dca020ccad40",
        "status": "successfull",
        "transferDuration": "00:1:23",
        "user": ObjectId("660b893a9f28ee9c2c007d06"),
    }

    time = datetime.datetime.now()
    prodcalls_collection.insert_one(document)
    print("Inserted @", time)

    s(20)

    prodcalls_collection.update_one(
        {"callId": "f072938a-8235-48cc-ba09-dca020ccad40",
            "expert": experts[0]},
        {"$set": {"status": "failed", "failedReason": "User not available"}})
    time = datetime.datetime.now()
    print("Updated @", time)

    s(5)

    prodcalls_collection.delete_one(
        {"callId": "f072938a-8235-48cc-ba09-dca020ccad40", "expert": experts[0]})
    print("Deleted")
