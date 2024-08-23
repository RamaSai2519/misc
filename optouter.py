from config import produsers_collection as collection
import pandas as pd

csv_file_path = 'xxxx.csv'
data = pd.read_csv(csv_file_path)
data_dict = data.to_dict(orient='records')

phone_numbers = data['phoneNumber'].tolist()
print(phone_numbers)

collection.update_many({'phoneNumber': {'$in': phone_numbers}}, {
                       '$set': {'wa_opt_out': True}})
