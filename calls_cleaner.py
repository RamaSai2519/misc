from config import prodcalls_collection
from pprint import pprint

calls = list(prodcalls_collection.find())

keys_to_remove = [
    "userSentiment",
    "Score Breakup",
    "timeSplit",
    "Customer Persona",
    "flow",
    "transcript_url",
    "Topics",
    "Saarthi Feedback",
    "User Callback",
    "Sentiment",
    "transcript",
    "tonality",
    "Conversation Score",
    "Summary",
    "closingGreeting",
    "openingGreeting",
    "probability",
    "timeSpent",
]

for call in calls:
    query = {"callId": call["callId"]}
    update = {"$unset": {key: "" for key in keys_to_remove}}
    prodcalls_collection.update_one(query, update)
    updated_document = prodcalls_collection.find_one(query)
    pprint(updated_document)

# query = {'_id': 'unique_document_id'}  # Replace with your document's unique identifier
# update = {'$unset': {'key_to_remove': ''}}  # Replace 'key_to_remove' with the key you want to drop
# collection.update_one(query, update)
# updated_document = collection.find_one(query)
# print(updated_document)
