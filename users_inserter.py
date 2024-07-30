import pytz
import pandas as pd
from datetime import datetime
from config import produsers_collection as collection
from config import prodmeta_collection as meta_collection

# Read the data from the CSV file
csv_file_path = 'leads.csv'
data = pd.read_csv(csv_file_path)

# Convert the DataFrame to a list of dictionaries
data_dict = data.to_dict(orient='records')

for record in data_dict:
    record['isBusy'] = False
    record['active'] = True
    record['isPaidUser'] = False
    record['createdAt'] = datetime.now(pytz.utc)
    record['numberOfCalls'] = 3
    record['numberOfGames'] = 0
    record['profileCompleted'] = False
    record['isBlocked'] = False

    inserted_record = collection.insert_one(record)
    inserted_id = inserted_record.inserted_id
    print(f"Inserted {record["name"]} with ID: {inserted_id}")

    meta_collection.insert_one({
        'user': inserted_id,
        'context': '',
        'source': 'zoom',
        'userStatus': '',
        'remarks': '',
    })
    print(f"Inserted meta data for {record["name"]}")
