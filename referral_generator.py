from config import devusers_collection as users_collection
from pymongo.collection import Collection
import hashlib
import random
import string


class Generator:
    def __init__(self) -> None:
        self.users_collection: Collection = users_collection

    def generate_referral_code(self, name: str, phone_number: str) -> str:
        salt = ''.join(random.choices(string.ascii_letters, k=6))
        raw_data = name + phone_number + salt
        hash_object = hashlib.sha256(raw_data.encode())
        code = hash_object.hexdigest()[:8].upper()
        valid_code = self.validate_referral_code(code)
        if not valid_code:
            return code
        print(f"Referral code {code} already exists. Generating new code...")
        self.generate_referral_code(name, phone_number)

    def validate_referral_code(self, referral_code: str) -> bool | dict:
        user = self.users_collection.find_one({"refCode": referral_code})
        return user if user else False


users = list(users_collection.find())
for user_data in users:
    if "refCode" not in user_data and user_data["profileCompleted"]:
        user_data["refCode"] = Generator().generate_referral_code(
            user_data["name"], user_data["phoneNumber"])
        users_collection.update_one(
            {"phoneNumber": user_data["phoneNumber"]},
            {"$set": user_data}
        )
        print("Successfully generated referral code for" +
              user_data['refCode'])
