from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

prod_client = MongoClient(os.getenv("PROD_DB_URL"))
prod_db = prod_client["test"]
calls_collection = prod_db["calls"]
callsmeta_collection = prod_db["callsmeta"]

calls = list(calls_collection.find())

for call in calls:
    if callsmeta_collection.find_one({"callId": call["callId"]}):
        continue
    elif "Conversation Score" in call:
        callId = call["callId"] if "callId" in call else ""
        user = call["user"] if "user" in call else ""
        expert = call["expert"] if "expert" in call else ""
        conversation_score = (
            call["Conversation Score"] if "Conversation Score" in call else 0
        )
        conversation_score_details = (
            call["Score Breakup"] if "Score Breakup" in call else ""
        )
        sentiment = call["Sentiment"] if "Sentiment" in call else ""
        saarthi_feedback = (
            call["Saarthi Feedback"] if "Saarthi Feedback" in call else ""
        )
        user_callback = call["User Callback"] if "User Callback" in call else ""
        topics = call["Topics"] if "Topics" in call else ""
        summary = call["Summary"] if "Summary" in call else ""
        transcript_url = call["transcript_url"] if "transcript_url" in call else ""
        callsmeta_collection.insert_one(
            {
                "callId": callId,
                "user": user,
                "expert": expert,
                "Conversation Score": conversation_score,
                "Score Breakup": conversation_score_details,
                "Sentiment": sentiment,
                "Saarthi Feedback": saarthi_feedback,
                "User Callback": user_callback,
                "Topics": topics,
                "Summary": summary,
                "transcript_url": transcript_url,
            }
        )
        print(f"Inserted {callId} into callsmeta collection")

print("Done copying calls to callsmeta collection")


"""
"callId": call["callId"],
"user": usercallId["_id"],
"expert": expert["_id"],
"Conversation Score": conversation_score,
"Score Breakup": conversation_score_details,
"Sentiment": sentiment,
"Saarthi Feedback": saarthi_feedback,
"User Callback": user_callback,
"Topics": topics,
"Summary": summary,
"transcript_url": transcript_url,
"""
