import pandas
from prerana_config import prusers_collection

file = 'paid.csv'

data = pandas.read_csv(file)
data_dicts = data.to_dict(orient='records')

unique_emails = set()

for record in data_dicts:
    user = {}
    user['name'] = record['Name']
    user['email'] = record['Email']
    user['phoneNumber'] = record['Mobile']
    user['gitamite'] = True

    if user['email'] in unique_emails:
        print(f"Duplicate email found: {user['email']}")
    else:
        prusers_collection.insert_one(user)
        unique_emails.add(user['email'])

print(f"Inserted {len(data_dicts)} records")
