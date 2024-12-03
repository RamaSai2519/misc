import requests
import pandas as pd
from datetime import datetime

csv_file_path = 'users.csv'

data = pd.read_csv(csv_file_path)

data_dict = data.to_dict(orient='records')
phone_numbers = data['phoneNumber'].tolist()

birthDate = datetime(2100, 1, 1).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

for phone in phone_numbers:
    payload = {
        'phoneNumber': str(phone),
        'birthDate': birthDate
    }
    response = requests.post(
        'http://localhost:8080/actions/user', json=payload)
    response_dict: dict = response.json()
    print(response_dict)
    message = response_dict.get('output_message')
    print(message)
