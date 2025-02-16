import os
import glob
import pandas as pd
from shared.db.users import get_user_collection

users_collection = get_user_collection()
csv_files = glob.glob(os.path.join(os.getcwd(), 'files', '*.csv'))
data = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
data_dict = data.to_dict(orient='records')


users = []

for item in data_dict:
    phone_number = item.get('phone_number')
    phone_number = phone_number.replace('p:', '').replace('+91', '').strip()

    query = {'phoneNumber': phone_number}
    projection = {'createdDate': 1, 'refSource': 1,
                  'name': 1, 'phoneNumber': 1}
    user = users_collection.find_one(query, projection)
    if user:
        user['createdDate'] = user['createdDate'].strftime(
            '%Y-%m-%d %H:%M:%S') + ' UTC'
        user.pop('_id')
        user['signed_up'] = True
        users.append(user)
    else:
        user = {
            'phoneNumber': phone_number,
            'name': item.get('name'),
            'signed_up': False,
        }
        users.append(user)

output_file = os.path.join(os.getcwd(), 'output', 'users.csv')
os.makedirs(os.path.dirname(output_file), exist_ok=True)
users_df = pd.DataFrame(users)
users_df.to_csv(output_file, index=False, encoding='utf-8')
