from config import prodexperts_collection, prodtimings_collection
from bson.objectid import ObjectId

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

times = [
    "PrimaryStartTime",
    "PrimaryEndTime",
    "SecondaryStartTime",
    "SecondaryEndTime"
]

expert = prodexperts_collection.find_one(
    {"_id": ObjectId("665ee53def29f5b2e07b1a80")})


for day in days:
    if day == "":
        prodtimings_collection.insert_one({
            "expert": expert["_id"], "day": day,
            times[0]: "", times[1]: "",
            times[2]: "", times[3]: ""
        })
        print(f"Inserted blank timings of {expert["name"]} for {day}")
    else:
        prodtimings_collection.insert_one({
            "expert": expert["_id"], "day": day,
            times[0]: "10:30", times[1]: "15:30",
            times[2]: "", times[3]: ""
        })
        print(f"Inserted timings of {expert["name"]} for {day}")
