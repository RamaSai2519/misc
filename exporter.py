from config import devcalls_collection
import pandas as pd

successful_calls = list(
    devcalls_collection.find({"failedReason": "", "status": "successfull"})
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
