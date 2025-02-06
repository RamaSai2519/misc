from shared.db.schedules import get_schedules_collection
from shared.db.experts import get_experts_collections
from shared.db.users import get_user_collection
from shared.models.constants import TimeFormats
from shared.configs import CONFIG as config
from datetime import datetime, timedelta
from bson import ObjectId
import pandas as pd
import requests

file = 'calls_to_be.csv'

calls_df = pd.read_csv(file)
calls_list = calls_df.to_dict(orient='records')
users_collection = get_user_collection()
experts_collection = get_experts_collections()
schedules_collection = get_schedules_collection()


def check_for_schedule(user_id: str, expert_id: str, job_time: datetime):
    query = {
        'job_time': job_time,
        'user_id': ObjectId(user_id),
        'expert_id': ObjectId(expert_id)
    }
    schedule = schedules_collection.find_one(query)
    return True if schedule else False


def schedule_call(user_id: str, expert_id: str, job_time: datetime):
    if check_for_schedule(user_id, expert_id, job_time) == True:
        print('call already scheduled')
        return 200

    job_time = job_time.strftime(TimeFormats.AWS_TIME_FORMAT)
    url = config.URL + '/actions/schedules'
    payload = {
        'job_type': 'CALL',
        'user_id': user_id,
        'job_time': job_time,
        'status': 'WAPENDING',
        'expert_id': expert_id,
        'user_requested': False,
        'initiatedBy': 'Rama Sathya Sai',
    }
    response = requests.post(url, json=payload)
    print(response.json(), '__response__')
    code = response.status_code
    if code != 200:
        output = response.json()
        msg = output.get('output_message')
        if msg == 'INVALID_INPUT. User is not interested':
            return 200
    return code


def get_user_id(phone_number: str) -> ObjectId:
    user = users_collection.find_one({'phoneNumber': phone_number})
    return user['_id']


def get_expert_id(name: str) -> str:
    expert = experts_collection.find_one({'name': name})
    return str(expert['_id'])


def get_slots(expert_id: str, job_time: datetime):
    url = config.URL + '/actions/slots'
    payload = {
        'expert': expert_id,
        'datetime': job_time.strftime(TimeFormats.ANTD_TIME_FORMAT),
        'duration': 30
    }
    response = requests.post(url, json=payload)
    slots = response.json()
    print(slots, '__slots__')
    slots = slots.get('output_details')
    if isinstance(slots, str):
        job_time += timedelta(days=1)
        return get_slots(expert_id, job_time)
    availables = []
    for slot in slots:
        availables.append(slot['available'])
    if not any(availables):
        job_time += timedelta(days=1)
        return get_slots(expert_id, job_time)
    return slots


for call in calls_list:
    user_name = str(call['name'])
    user_number = str(call['phoneNumber'])
    sarathi_name = str(call['sarathi']).strip()
    expert_id = get_expert_id(sarathi_name)
    user_id = get_user_id(user_number)

    user_id = str(user_id)
    start_time = datetime(2025, 2, 9, 0, 0, 0)
    while True:
        slots = get_slots(expert_id, start_time)
        max = len(slots)
        i = 0
        for slot in slots:
            i += 1
            if slot['available'] == True:
                job_time = datetime.strptime(
                    slot['datetime'], TimeFormats.ANTD_TIME_FORMAT)
                code = schedule_call(user_id, expert_id, job_time)
                if code == 200:
                    print(f'Scheduled for {user_name} with {sarathi_name}')
                    break
            if i == max:
                start_time += timedelta(days=1)
        else:
            continue
        break
