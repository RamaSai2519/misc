from config import prod_db, dev_db

prod_collections = list(prod_db.list_collection_names())

for collection_name in prod_collections:
    if collection_name not in [""]:
        prod_collection = prod_db.get_collection(collection_name)
        dev_collection = dev_db.get_collection(collection_name)
        dev_collection.drop()
        print(f"Copying {collection_name} from prod to dev")
        documents = list(prod_collection.find().sort("_id", -1))
        if documents and len(documents) > 0:
            update = dev_collection.insert_many(documents)
            print(f"Copied {len(documents)} documents to {collection_name} in dev")
        else:
            print(f"No documents found in {collection_name} in prod")
