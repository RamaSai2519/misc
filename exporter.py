from config import produsers_collection, prodcalls_collection
import pandas as pd

users = list(produsers_collection.find())
active_users = []
for user in users:
    if prodcalls_collection.find_one({"user": user["_id"]}):
        active_users.append(user)


df = pd.DataFrame(active_users)

# Export the data to an Excel file
df.to_excel("callactiveusers.xlsx", index=False)
