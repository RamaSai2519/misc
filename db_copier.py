from pymongo import MongoClient

prod_client = MongoClient(
    "mongodb+srv://sukoon_user:Tcks8x7wblpLL9OA@cluster0.o7vywoz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
dev_client = MongoClient(
    "mongodb+srv://techcouncil:2lfNFMZIjdfZJl2R@cluster0.h3kssoa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
prod_db = prod_client["test"]
dev_db = dev_client["test"]

prod_collections = list(prod_db.list_collection_names())

for collection_name in prod_collections:
    if collection_name == "events" or collection_name == "eventconfigs":
        continue
    else:
        prod_collection = prod_db.get_collection(collection_name)
        dev_collection = dev_db.get_collection(collection_name)
        dev_collection.drop()
        print(f"Copying {collection_name} from prod to dev")
        documents = list(prod_collection.find())
        for document in documents:
            dev_collection.insert_one(document)