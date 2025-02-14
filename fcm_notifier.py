import os
import requests
import pandas as pd
from shared.configs import CONFIG as config

csv_file_path = os.path.join(os.getcwd(), 'tokens.csv')
data = pd.read_csv(csv_file_path)
data = data.to_dict(orient='records')


message = "Hello, {name}!."

for record in data:
    name = record.get('name')
    message = message.format(name=name)

    url = config.URL + '/actions/push'
    payload = {
        'token': record.get('token'),
        'type_': 'user',
        'sound': 'bell',  # test which is working
        'app_type': 'user',
        'priority': 'high',
        'title': 'Test',
        'body': message,
    }
    response = requests.post(url, json=payload)
    print(response.text)
