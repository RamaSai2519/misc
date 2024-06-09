from config import devusers_collection, devmeta_collection
import csv
from bson import ObjectId


# Function to convert context string to dictionary
def parse_context(context_str):
    context_dict = {}
    context_lines = context_str.split("\n")
    for line in context_lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            context_dict[key.strip()] = value.strip()
    return context_dict


# Read the CSV file and update the database
with open("users_context.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        phone_number = row[0]
        user = devusers_collection.find_one({"phoneNumber": phone_number})
        user_id = user["_id"] if user else None
        if user:
            context_dict = parse_context(row[1])
            context_dict["user"] = ObjectId(user_id)
            devmeta_collection.insert_one(context_dict)
            print(f"Updated context for {phone_number}")
        else:
            print(f"User with phone number {phone_number} not found")


# client = MongoClient(
#     "mongodb+srv://sukoon_user:Tcks8x7wblpLL9OA@cluster0.o7vywoz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# )
