import os
import glob
import pandas as pd
from datetime import datetime
from config import produsers_collection as collection
from config import prodmeta_collection as meta_collection

# Get all CSV files in the 'files' folder of the working directory
csv_files = glob.glob(os.path.join(os.getcwd(), 'files', '*.csv'))

# Concatenate all CSV files together
data = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Convert the DataFrame to a list of dictionaries
data_dict = data.to_dict(orient='records')

for record in data_dict:
    user_dict = {}
    if len(str(record["Phone"])) != 10:
        print(f"Phone number {record["Phone"]} is invalid")
        continue
    existing_user = collection.find_one(
        {"phoneNumber": str(record["Phone"])})
    if existing_user:
        print(f"User with phone number {record["Phone"]} already exists")
        continue

    user_dict['name'] = str(record["First Name"] +
                            record["Last Name"]).strip()
    user_dict['email'] = str(record["Email"]).strip()

    try:
        user_joined_date = datetime.strptime(
            str(record["Registration Time"]), "%Y-%m-%d %H:%M:%S")
    except:
        user_joined_date = datetime.now()

    user_dict['isBusy'] = False
    user_dict['active'] = True
    user_dict['isPaidUser'] = False
    user_dict['createdDate'] = user_joined_date
    user_dict['numberOfCalls'] = 3
    user_dict['numberOfGames'] = 0
    user_dict['profileCompleted'] = False
    user_dict['isBlocked'] = False
    user_dict["phoneNumber"] = str(record["Phone"])

    inserted_record = collection.insert_one(user_dict)
    inserted_id = inserted_record.inserted_id
    print(f"Inserted {user_dict["name"]} with ID: {inserted_id}")

    meta_collection.insert_one({
        'user': inserted_id,
        'context': str(record["Webinar"]).strip(),
        'source': 'zoom',
        'userStatus': '',
        'remarks': '',
    })
    print(f"Inserted meta data for {user_dict["name"]}")
