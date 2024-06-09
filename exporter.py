from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

prod_client = MongoClient(os.getenv("DEV_DB_URL"))
db = prod_client["test"]
calls_collection = db["calls"]

successful_calls = list(
    calls_collection.find({"failedReason": "", "status": "successfull"})
)

data = []
for call in successful_calls:
    callId = call["callId"]
    duration = call["duration"]
    durationInSeconds = call["durationInSeconds"]
    data.append(
        {"callId": callId, "duration": duration, "durationInSeconds": durationInSeconds}
    )

df = pd.DataFrame(data)

# Export the data to an Excel file
df.to_excel("exported_data.xlsx", index=False)
