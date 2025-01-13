from config import prod_client

db = prod_client['embeddings']

old_name = 'system_prompts'
new_name = 'prompt_proposals'

old_collection = db[old_name]
new_collection = db[new_name]

new_collection.drop()
query = {}
documents = list(old_collection.find(query))
if documents and len(documents) > 0:
    update = new_collection.insert_many(documents)
    print(f"Copied {len(documents)} documents")
else:
    print(f"No documents found")
