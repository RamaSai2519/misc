from config import prodexperts_collection, prodcategories_collection

experts = list(prodexperts_collection.find())
cats_in_use = []

for expert in experts:
    categories = expert["categories"]
    for cat in categories:
        if cat not in cats_in_use:
            cats_in_use.append(cat)

categories = list(prodcategories_collection.find())

for cat in categories:
    if cat["_id"] not in cats_in_use:
        prodcategories_collection.delete_one({"_id": cat["_id"]})
        print(f"Deleted {cat['name']}")
    else:
        print(f"Kept {cat['name']}")

print("Done")
