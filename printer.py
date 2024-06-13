from config import prodevents_collection

events = list(prodevents_collection.find())

for event in events:
    phone_numbers = set()
    for event in events:
        phone_number = event['phoneNumber']
        if phone_number in phone_numbers:
            print(event)
        else:
            phone_numbers.add(phone_number)
