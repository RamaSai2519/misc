from config import prodmeta_collection as meta_collection
from config import produsers_collection as collection

users = list(collection.find())
metas = list(meta_collection.find())
user_ids = [user["_id"] for user in users]

for meta in metas:
    if meta.get("user") not in user_ids:
        meta_collection.delete_one({"_id": meta["_id"]})
        print(f"Deleted meta data for user {meta.get('user')}")
