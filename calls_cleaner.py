from config import prodmeta_collection

meta = list(prodmeta_collection.find({
    "expert": {"$exists": True}
}))

for m in meta:
    if m["expert"] == "Unknown":
        print(m["user"], m["expert"])
        prodmeta_collection.update_one(
            {"_id": m["_id"]},
            {"$set": {"expert": "N/A"}}
        )
