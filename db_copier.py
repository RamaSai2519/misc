from config import prod_client


dbs = prod_client.list_database_names()

for db_name in dbs:
    if db_name in ['smr_agro']:
        prod_db = prod_client[db_name]
        dev_db = prod_client['smr_agro_dev']
        prod_collections = list(prod_db.list_collection_names())
        for collection in prod_collections:
            if collection not in ['']:
                prod_collection = prod_db.get_collection(collection)
                dev_collection = dev_db.get_collection(collection)
                dev_collection.drop()
                print(f'Copying {collection} from prod to dev')
                docs_cursor = prod_collection.find().sort('_id', -1)
                if 'user' not in collection:
                    docs_cursor = docs_cursor.limit(1000)

                docs = list(docs_cursor)
                if docs:
                    update = dev_collection.insert_many(docs)
                    print(f'Copied {len(docs)} docs to {collection} in dev')
                else:
                    print(f'No documents found in {collection} in prod')
