from pymongo import MongoClient

# Connect to the MongoDB client
dev_client = MongoClient(
    "mongodb+srv://techcouncil:2lfNFMZIjdfZJl2R@cluster0.h3kssoa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = dev_client["test"]
meta_collection = db["meta"]


# Function to find all unique keys in a collection
def find_unique_keys(collection):
    unique_keys = set()
    cursor = collection.find()
    for document in cursor:
        unique_keys.update(document.keys())
    return unique_keys


# Example usage
unique_keys = find_unique_keys(meta_collection)
print("Unique keys in the collection:")
for key in unique_keys:
    print(key)
