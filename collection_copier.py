from config import prod_client

db = prod_client['embeddings']

old_name = 'histories'
new_name = 'old_histories'

old_collection = db[old_name]
new_collection = db[new_name]

new_collection.drop()
query = {"createdAt": {"$regex": "^.{11,}$"}}
documents = list(old_collection.find(query))
if documents and len(documents) > 0:
    update = new_collection.insert_many(documents)
    print(f"Copied {len(documents)} documents")
else:
    print(f"No documents found")
