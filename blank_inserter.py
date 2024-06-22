from config import prodtimings_collection
from bson import ObjectId

# experts = list(prodexperts_collection.find({}))

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

# for expert in experts:
for day in days:
    # if prodtimings_collection.find_one({"expert": expert["_id"], "day": day}):
    #     continue
    prodtimings_collection.insert_one(
        {"expert": ObjectId("665ee53def29f5b2e07b1a80"), "day": day,
         "PrimaryStartTime": "10:30", "PrimaryEndTime": "15:30",
            # "SecondaryStartTime": "17:00", "SecondaryEndTime": "19:00"
         })
    print(f"Inserted timings for {day}")
