from shared.db.users import get_user_collection
from shared.configs import CONFIG as config
from shared.models.common import Common
from datetime import datetime
import requests

users_collection = get_user_collection()

query = {
    'name': {'$exists': True, '$ne': ''},
    '$or': [
        # {'birthDate': {'$exists': False}},
        # {'birthDate': {'$eq': None}},
        {'city': {'$exists': False}},
        {'city': {'$eq': None}}
    ]
}

user_phones = users_collection.distinct('phoneNumber', query)

url = config.URL + '/actions/user'

for phone in user_phones:
    payload = {
        'phoneNumber': phone,
        # 'birthDate': datetime(1900, 1, 1),
        'city': 'unknown'
    }
    payload = Common.jsonify(payload)
    response = requests.post(url, json=payload)
    print(response.text)
