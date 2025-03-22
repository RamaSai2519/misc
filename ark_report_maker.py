from shared.db.chat import get_histories_collection
from datetime import datetime
import csv

collection = get_histories_collection()

query = {'createdDate': {'$gte': datetime(2024, 12, 1)}}
phones = collection.distinct('phoneNumber', query)

docs = []

for phone in phones:
    query = {'phoneNumber': phone}
    project = {'createdAt': 1, 'phoneNumber': 1, 'createdDate': 1}
    doc = list(collection.find(query, project).sort(
        'createdDate', -1).limit(1))[0]
    docs.append({
        'phoneNumber': phone,
        'createdDate': doc['createdAt']
    })


with open('output1.csv', 'w', newline='') as csvfile:
    fieldnames = ['phoneNumber', 'createdDate']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for doc in docs:
        writer.writerow(doc)
