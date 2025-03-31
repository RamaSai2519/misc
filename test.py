from shared.db.users import get_user_collection, get_meta_collection
from shared.db.chat import get_histories_collection
import numpy as np


meta_collection = get_meta_collection()
users_collection = get_user_collection()
histories_collection = get_histories_collection()


query = {'userStatus': {
    '$in': ['not_interested_user', 'not_interested_calls_user']}}
user_ids = meta_collection.distinct('user', query)

user_phones = users_collection.distinct(
    'phoneNumber', {'_id': {'$in': user_ids}})

docs = []
for phone in user_phones:
    query = {'phoneNumber': phone}
    doc = histories_collection.find_one(query)
    if doc:
        docs.append(phone)

output_file = 'output.csv'
np.savetxt(output_file, docs, delimiter=",", fmt='%s',
           header="PhoneNumber", comments='')
print(f"Exported {len(docs)} phone numbers to {output_file}")
