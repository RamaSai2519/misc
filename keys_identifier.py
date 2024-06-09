from config import devcalls_collection


def get_all_unique_keys(collection):
    unique_keys = set()

    # Iterate through all documents in the collection
    for document in collection.find():
        unique_keys.update(document.keys())

    return unique_keys


def main():
    # Get all unique keys
    unique_keys = get_all_unique_keys(devcalls_collection)

    # Print unique keys
    print("Unique keys in the collection:")
    for key in unique_keys:
        print(key)


if __name__ == "__main__":
    main()
