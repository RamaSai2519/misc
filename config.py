from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

prod_client = MongoClient(os.getenv("PROD_DB_URL"))
prod_db = prod_client["test"]

dev_client = MongoClient(os.getenv("DEV_DB_URL"))
dev_db = dev_client["test"]

prodcalls_collection = prod_db["calls"]
prodcallsmeta_collection = prod_db["callsmeta"]
prodschedules_collection = prod_db["schedules"]
produsers_collection = prod_db["users"]
prodexperts_collection = prod_db["experts"]
prodmeta_collection = prod_db["meta"]
prodevents_collection = prod_db["events"]
prod_timings_collection = prod_db["timings"]

devcalls_collection = dev_db["calls"]
devcallsmeta_collection = dev_db["callsmeta"]
devschedules_collection = dev_db["schedules"]
devusers_collection = dev_db["users"]
devexperts_collection = dev_db["experts"]
devmeta_collection = dev_db["meta"]
