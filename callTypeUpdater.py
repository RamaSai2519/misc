from config import prodschedules_collection, prodcalls_collection
from datetime import timedelta

# Find all schedules
schedules = list(prodschedules_collection.find())

for schedule in schedules:
    schedule_user = schedule["user"]
    schedule_expert = schedule["expert"]

    # Adjust schedule time to match call time (assuming your schedule time is in UTC and call time is in local time)
    schedule_time = schedule["datetime"] - timedelta(hours=5, minutes=30)

    # Find calls for the same user and expert within a small time window around the schedule time
    calls = list(
        prodcalls_collection.find(
            {
                "user": schedule_user,
                "expert": schedule_expert,
                "initiatedTime": {
                    "$gte": schedule_time - timedelta(minutes=1),
                    "$lte": schedule_time + timedelta(minutes=1),
                },
            }
        )
    )

    if calls:
        prodschedules_collection.update_one(
            {"_id": schedule["_id"]}, {"$set": {"status": "successful"}}
        )
        for call in calls:
            # Update the call type in the database
            call_type = "scheduled"
            prodcalls_collection.update_one(
                {"_id": call["_id"]}, {"$set": {"type": call_type}}
            )
            print(f"Updated call type for call initiated at {call['initiatedTime']}")
    else:
        print(
            f"No calls found for user {schedule_user} and expert {schedule_expert} around schedule time {schedule['datetime']}"
        )
