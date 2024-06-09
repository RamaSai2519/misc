from config import produsers_collection, prodmeta_collection
import csv
from bson import ObjectId


# Function to parse the context string and separate 'Source' field
def parse_context(context_str):
    context_lines = context_str.split("\n")
    source = None
    context_parts = []
    for line in context_lines:
        if line.startswith("Source:"):
            source = line.split("Source:", 1)[1].strip()
        elif line.startswith(" Source:"):
            source = line.split(" Source:", 1)[1].strip()
        elif line.startswith("source:"):
            source = line.split("source:", 1)[1].strip()
        elif line.startswith(" source:"):
            source = line.split(" source:", 1)[1].strip()
        elif line.startswith("Source :"):
            source = line.split("Source :", 1)[1].strip()
        else:
            context_parts.append(line)
    context = "\n".join(context_parts).strip()
    return context, source


# Read the CSV file and update the database
with open("contexts.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        phone_number = row[0]
        user = produsers_collection.find_one({"phoneNumber": phone_number})
        user_id = user["_id"] if user else None
        if user:
            context, source = parse_context(row[1])
            document = {"user": ObjectId(user_id), "context": context}
            if source:
                document["source"] = source
            prodmeta_collection.insert_one(document)
            print(f"Updated context for {phone_number}")
        else:
            print(f"User with phone number {phone_number} not found")
