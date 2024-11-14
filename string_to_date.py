from config import produsers_collection as collection
from datetime import date, datetime
import pytz

query = {"createdDate": {"$type": "string"}}

users: list[dict] = collection.find(
    query, {"createdDate": 1, "phoneNumber": 1, "name": 1})


def string_to_date(doc: dict, field: str) -> date:
    if field in doc and doc[field] is not None and isinstance(doc[field], str):
        try:
            doc[field] = datetime.strptime(
                doc[field], '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            doc[field] = datetime.now(pytz.utc)
    return doc[field]


updates = 0

for user in users:
    user['createdDate'] = string_to_date(user, 'createdDate')
    update = collection.update_one({"_id": user["_id"]}, {
        "$set": {"createdDate": user["createdDate"]}})
    if update.modified_count > 0:
        print(f"Updated user: {user.get('name', user.get('phoneNumber', 'Unknown'))}")
        updates += 1
    else:
        print(f"User not updated: {user.get('name', user.get('phoneNumber', 'Unknown'))}")

print(f"Total updates: {updates}")
