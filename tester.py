from config import prodcalls_collection
import os
from time import sleep as s

doc = os.getenv("DOC")

prodcalls_collection.insert_one(doc)
print("Inserted")

s(5)

prodcalls_collection.delete_one({"callId": "f072938a-8235-48cc-ba09-dca020ccad40"})
print("Deleted")
