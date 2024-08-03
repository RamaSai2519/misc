from config import produsers_collection as users_collection
from config import prodmeta_collection as meta_collection
from config import prodevents_collection as events_collection
import time

while True:
    print("Running the migration script")
    signedUpUsers = list(users_collection.find().sort("createdDate", -1))
    signedUpPhoneNumbers = [user["phoneNumber"]
                            for user in signedUpUsers]

    allEventUsersQuery = {"phoneNumber": {"$nin": signedUpPhoneNumbers}}
    allEventUsers = list(events_collection.find(
        allEventUsersQuery).sort("createdAt", -1))
    print(f"Found {len(allEventUsers)} event users")

    for eventUser in allEventUsers:
        user_doc = {
            "name": eventUser["name"] if "name" in eventUser else "",
            "phoneNumber": eventUser["phoneNumber"],
            "city": eventUser["city"] if "city" in eventUser else "",
            "birthDate": eventUser["dob"] if "dob" in eventUser else "",
            "createdDate": eventUser["createdAt"],
            "isBusy": False,
            "active": True,
            "isPaidUser": False,
            "numberOfCalls": 3,
            "numberOfGames": 0,
            "profileCompleted": False,
            "isBlocked": False,
            "otp": "",
            "expiresOtp": "",
        }
        inserted_record = users_collection.insert_one(user_doc)
        inserted_id = inserted_record.inserted_id
        user_name = eventUser["name"] if "name" in eventUser else eventUser["phoneNumber"]
        print(
            f"Inserted {user_name} with ID: {inserted_id} in users collection")

        usermeta_doc = {
            "user": inserted_id,
            "context": "",
            "source": "Events",
            "userStatus": "",
            "remarks": "",
            "email": eventUser["email"] if "email" in eventUser else "",
        }
        inserted_id = meta_collection.insert_one(usermeta_doc)
        print(
            f"Inserted meta data for {user_name} with ID: {inserted_id} in meta collection")

    print("sleeping")
    time.sleep(7200)
