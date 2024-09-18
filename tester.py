from config import devcalls_collection as collection
from time import sleep as s
from bson import ObjectId
import datetime

document = {
    "callId": "2f8eb444-09df-4b5e-ae48-ed2628f01e2d",
    "duration": "0:05:51",
    "expert": ObjectId("6604694542f04a057fa2100f"),
    "failedReason": "",
    "initiatedTime": datetime.datetime(2024, 9, 18, 11, 32, 29, 127000),
    "recording_url": "https://sr.knowlarity.com/vr/fetchsound/?callid%3D2f8eb444-09df-4b5e-ae48-ed2628f01e2d",
    "status": "successfull",
    "transferDuration": "00:05:39",
    "user": ObjectId("66c828b7dff284cbc80223e7"),
}

time = datetime.datetime.now()
collection.insert_one(document)
print("Inserted @", time)

s(20)

collection.update_one(
    {"callId": "f072938a-8235-48cc-ba09-dca020ccad40",
     "expert": ObjectId("6604694542f04a057fa2100f")},
    {"$set": {"status": "failed", "failedReason": "User not available"}})
time = datetime.datetime.now()
print("Updated @", time)

s(5)

collection.delete_one({"callId": "f072938a-8235-48cc-ba09-dca020ccad40"})
print("Deleted")
