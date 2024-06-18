from pymongo import MongoClient
from datetime import timedelta, datetime
from time import sleep

# Connect to the database
client = MongoClient(
    "mongodb+srv://sukoon_user:Tcks8x7wblpLL9OA@cluster0.o7vywoz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["test"]
prodschedules_collection = db["schedules"]
prodcalls_collection = db["calls"]

while True:
    # Find all schedules
    schedules = list(prodschedules_collection.find({"status": "pending"}))

    print("Checking for schedules...")
    for schedule in schedules:
        schedule_user = schedule["user"]
        schedule_expert = schedule["expert"]

        # Adjust schedule time to match call time (assuming your schedule time is in IST and call time is in UTC)
        schedule_time = schedule["datetime"] - timedelta(hours=5, minutes=30)

        # Find calls for the same user and expert within a small time window around the schedule time
        calls = list(
            prodcalls_collection.find(
                {
                    "user": schedule_user,
                    "expert": schedule_expert,
                    "initiatedTime": {
                        "$gte": schedule_time - timedelta(minutes=1),
                        "$lte": schedule_time + timedelta(minutes=1)
                    },
                }
            )
        )

        if calls:
            prodschedules_collection.update_one(
                {"_id": schedule["_id"]}, {"$set": {"status": "completed"}}
            )
            for call in calls:
                # Update the call type in the database
                call_type = "scheduled"
                prodcalls_collection.update_one(
                    {"_id": call["_id"]}, {"$set": {"type": call_type}}
                )
                print(
                    f"Updated call type for call initiated at {
                        call['initiatedTime']}"
                )
        else:
            if (schedule_time + timedelta(hours=5, minutes=30)) < datetime.now():
                print(schedule_time, datetime.now())
                prodschedules_collection.update_one(
                    {"_id": schedule["_id"]}, {"$set": {"status": "missed"}}
                )
            else:
                prodschedules_collection.update_one(
                    {"_id": schedule["_id"]}, {"$set": {"status": "pending"}}
                )

    # Sleep for 2 minutes before checking again
    sleep(60)
