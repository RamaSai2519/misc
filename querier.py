from shared.db.events import get_contribute_events_collection

collection = get_contribute_events_collection()

query = {'slug': 'aut'}
update = {'$set': {'isSukoon': True}}
doc = collection.update_one(query, update)
print(doc)
