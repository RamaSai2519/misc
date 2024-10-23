import requests
from config import produsers_collection

query = {'customerPersona': {'$type': "object"}}
users = produsers_collection.find(query).skip(16).limit(1)

for user in users:
    url = "http://localhost:8080/actions/recommend_expert"
    payload = {'user_id': str(user['_id'])}
    response = requests.post(url, json=payload)
    expert_name = response.json().get('output_details', {}).get('name', None)
    message = response.json().get('output_message', None)
    print(f"Expert for user {user['name']}: {expert_name} - {message}")
