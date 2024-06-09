from config import devmeta_collection


# Function to find all unique keys in a collection
def find_unique_keys(collection):
    unique_keys = set()
    cursor = collection.find()
    for document in cursor:
        unique_keys.update(document.keys())
    return unique_keys


# Example usage
unique_keys = find_unique_keys(devmeta_collection)
print("Unique keys in the collection:")
for key in unique_keys:
    print(key)
