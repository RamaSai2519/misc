from config import prodcalls_collection
from pprint import pprint

doc = prodcalls_collection.find_one({"callId": "d1a4d508-80c4-4861-b319-814f66470a00"})

pprint(doc)