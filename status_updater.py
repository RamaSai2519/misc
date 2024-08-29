from config import dev_client as client, FCM_SERVER_KEY
from datetime import datetime, timedelta
import requests
import time
import pytz
import jwt

db = client["test"]
experts_collection = db["experts"]
fcm_tokens_collection = db["fcm_tokens"]
errorlog_collection = db["errorlogs"]


def notify(message):
    fcm_url = "https://fcm.googleapis.com/fcm/send"
    server_key = str(FCM_SERVER_KEY)
    datetime_now = datetime.now(pytz.timezone("Asia/Kolkata"))
    current_time = datetime_now.strftime("%Y-%m-%d %H:%M:%S")
    errorlog_collection.insert_one({"message": message, "time": current_time})
    tokens = list(fcm_tokens_collection.find())
    for token in tokens:
        payload = {
            "to": token["token"],
            "notification": {"title": "Notification", "body": message},
        }
        headers = {
            "Authorization": "key=" + server_key,
            "Content-Type": "application/json",
        }
        response = requests.post(fcm_url, json=payload, headers=headers)
    if response.status_code == 200:
        pass
    else:
        print("Failed to send notification:", response.text)


def generate_token(expert):
    payload = {
        "name": expert["name"],
        "userId": str(expert["_id"]),
        "phoneNumber": expert["phoneNumber"],
    }
    token = jwt.encode(payload, "saltDemaze", algorithm="HS256")
    return token


def job():
    experts = list(experts_collection.find({"status": "online"}))
    admin_url = "https://rama.sukoonunlimited.com/admin/expert/updateStatus"
    for expert in experts:
        token = generate_token(expert)
        payload = {"expertId": token, "status": "offline"}
        headers = {"Content-Type": "application/json"}
        response = requests.post(admin_url, headers=headers, json=payload)
        if response.status_code == 200:
            pass
        else:
            notify(f"Failed to update status of {expert['name']}")
    datetime_now = datetime.now(pytz.timezone("Asia/Kolkata"))
    notify(
        f"All Saarthis are offline now at {
            datetime_now.hour}:{datetime_now.minute}"
    )


while True:
    print("started")
    current_time = datetime.now(pytz.timezone("Asia/Kolkata"))
    target_time = current_time.replace(
        hour=22, minute=0, second=0, microsecond=0)
    if current_time > target_time:
        target_time = target_time + timedelta(days=1)
    sleep_duration = (target_time - current_time).total_seconds()
    time.sleep(sleep_duration)
    job()
