from config import devcalls_collection
from pprint import pprint
import time

calls = list(devcalls_collection.find())

keys_to_remove = [
    "Conversation Score",
    "Saarthi Feedback",
    "Score Breakup",
    "Sentiment",
    "Summary",
    "Topics",
    "User Callback",
    "closingGreeting",
    "flow",
    "timeSpent",
    "tonality",
    "userSentiment",
    "openingGreeting",
    "probability",
    "timeSplit",
]

for call in calls:
    for key in keys_to_remove:
        if key in call:
            del call[key]
    devcalls_collection.update_one({"callId": call["callId"]}, {"$set": call})
    pprint(call)
