from config import prodcalls_collection

query = {"failedReason": "user missed"}
calls = list(prodcalls_collection.find(query))


def duration_str_to_seconds(duration: str) -> int:
    duration = duration.split(':')
    hours, minutes, seconds = map(int, duration)
    return hours * 3600 + minutes * 60 + seconds


callIds = [call['callId'] for call in calls]

update = prodcalls_collection.update_many(
    {"callId": {"$in": callIds}}, {
        "$set": {"status": "missed"}}
)
print(update)
print(f"Updated {update.modified_count} calls")
