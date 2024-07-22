from config import prodevents_collection
import pandas as pd

moved_users = list(
    prodevents_collection.find({"user_id": {"$exists": True}})
)

df = pd.DataFrame(moved_users)

# Export the data to an Excel file
df.to_excel("exported_data.xlsx", index=False)
