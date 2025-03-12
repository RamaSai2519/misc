from shared.db.schedules import get_schedules_collection
from shared.db.experts import get_experts_collections
from shared.db.users import get_user_collection
from shared.models.constants import TimeFormats
from shared.configs import CONFIG as config
from datetime import datetime, timedelta
from shared.models.common import Common
from bson import ObjectId
import pandas as pd
import requests
import pytz
import time


class Scheduler:
    def __init__(self, file: str) -> None:
        self.calls_df = pd.read_csv(file)
        self.calls_list = self.calls_df.to_dict(orient='records')
        self.users_collection = get_user_collection()
        self.experts_collection = get_experts_collections()
        self.schedules_collection = get_schedules_collection()

    def check_for_schedule(self, user_id: str, expert_id: str, job_time: datetime):
        query = {
            'job_time': job_time,
            'user_id': ObjectId(user_id),
            'expert_id': ObjectId(expert_id)
        }
        schedule = self.schedules_collection.find_one(query)
        return True if schedule else False

    def schedule_call(self, user_id: str, expert_id: str, job_time: datetime):
        if self.check_for_schedule(user_id, expert_id, job_time):
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

        common = Common()
        balance = common.get_balance_type(expert_id)
        token = Common.get_token(user_id, balance)
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.post(url, json=payload, headers=headers)
        print(response.json(), '__response__')
        code = response.status_code
        if code != 200:
            output = response.json()
            msg = output.get('output_message')
            if msg == 'INVALID_INPUT. User is not interested':
                return 200
        return code

    def get_user_id(self, phone_number: str) -> ObjectId:
        user = self.users_collection.find_one({'phoneNumber': phone_number})
        return None if not user else str(user['_id'])

    def get_expert_id(self, number: str) -> str:
        expert = self.experts_collection.find_one({'phoneNumber': number})
        if not expert:
            return None
        if expert.get('type', 'saarthi') != 'saarthi':
            print(f'Expert {number} is not a saarthi')
            time.sleep(5)
            return None
        return str(expert['_id'])

    def get_slots(self, expert_id: str, job_time: datetime):
        url = config.URL + '/actions/slots'
        payload = {
            'expert': expert_id,
            'datetime': job_time.strftime(TimeFormats.ANTD_TIME_FORMAT),
            'duration': 60
        }
        response = requests.post(url, json=payload)
        slots = response.json()
        print(slots, '__slots__')
        slots = slots.get('output_details')
        if isinstance(slots, str):
            job_time += timedelta(days=1)
            return self.get_slots(expert_id, job_time)
        availables = []
        for slot in slots:
            availables.append(slot['available'])
        if not any(availables):
            job_time += timedelta(days=1)
            return self.get_slots(expert_id, job_time)
        return slots

    def run(self) -> None:
        for call in self.calls_list:
            user_number = str(call['user']).strip()
            sarathi_number = str(call['saarthi']).strip()
            expert_id = self.get_expert_id(sarathi_number)
            user_id = self.get_user_id(user_number)
            if not expert_id or not user_id:
                print('Invalid user or expert')
                continue

            start_time = datetime(2025, 2, 18, 0, 0, 0, tzinfo=pytz.utc)
            current_time = Common.get_current_utc_time()
            if start_time < current_time:
                start_time = current_time
            while True:
                slots = self.get_slots(expert_id, start_time)
                max = len(slots)
                i = 0
                for slot in slots:
                    i += 1
                    if slot['available']:
                        job_time = datetime.strptime(
                            slot['datetime'], TimeFormats.ANTD_TIME_FORMAT)
                        code = self.schedule_call(user_id, expert_id, job_time)
                        if code == 200:
                            print(
                                f'Scheduled for {user_number} with {sarathi_number}')
                            break
                    if i == max:
                        start_time += timedelta(days=1)
                else:
                    continue
                break


if __name__ == "__main__":
    scheduler = Scheduler('calls_to_be.csv')
    scheduler.run()
