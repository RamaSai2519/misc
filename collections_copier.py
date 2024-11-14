from config import prod_client, prod_db

old_db = prod_db
new_db = prod_client["events"]


def create_dict(old: str, new: str) -> dict[str, str]:
    return {'old': old, 'new': new}


collections = [
    create_dict('eventconfigs', 'events'),
    create_dict('events', 'event_users')
]

for collection in collections:
    old_collection = old_db[collection['old']]
    new_collection = new_db[collection['new']]
    old_documents = list(old_collection.find())
    new_collection.drop()
    new_collection.insert_many(old_documents)
