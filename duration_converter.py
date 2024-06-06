from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

dev_client = MongoClient(os.getenv("DEV_DB_URL"))
db = dev_client["test"]
calls_collection = db["calls"]

calls = list(calls_collection.find())


def format_duration(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    print(f"{time_str} -> {hours * 3600 + minutes * 60 + seconds}")
    return hours * 3600 + minutes * 60 + seconds


total_calls = len(calls)
for index, call in enumerate(calls):
    if "durationInSeconds" in call or "duration" not in call or call["duration"] == "":
        continue
    call_duration = call["duration"]
    formatted_duration = format_duration(call_duration)
    calls_collection.update_one(
        {"callId": call["callId"]}, {"$set": {"durationInSeconds": formatted_duration}}
    )
    percentage = (index + 1) / total_calls * 100
    print(f"Progress: {percentage:.2f}%")
