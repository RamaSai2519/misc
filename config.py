from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

prod_client = MongoClient(os.getenv("PROD_DB_URL"))
prod_db = prod_client["test"]

dev_client = MongoClient(os.getenv("DEV_DB_URL"))
dev_db = dev_client["test"]

FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY")

produserreferrals_collection = prod_db["userreferrals"]
prodeventconfigs_collection = prod_db["eventconfigs"]
prodcategories_collection = prod_db["categories"]
prodcallsmeta_collection = prod_db["callsmeta"]
prodschedules_collection = prod_db["schedules"]
prodexperts_collection = prod_db["experts"]
prodtimings_collection = prod_db["timings"]
prodevents_collection = prod_db["events"]
prodcalls_collection = prod_db["calls"]
produsers_collection = prod_db["users"]
prodmeta_collection = prod_db["meta"]


devuserreferrals_collection = dev_db["userreferrals"]
devcallsmeta_collection = dev_db["callsmeta"]
devschedules_collection = dev_db["schedules"]
devexperts_collection = dev_db["experts"]
devtimings_collection = dev_db["timings"]
devcalls_collection = dev_db["calls"]
devusers_collection = dev_db["users"]
devmeta_collection = dev_db["meta"]
