import pandas as pd
from datetime import datetime, timedelta
from config import produsers_collection

# Sample data: array of dicts
users = list(produsers_collection.find())

# Get the minimum createdDate to determine the start of the first week
min_date = min(user['createdDate'] for user in users)

# Function to get the start of the week based on the minimum date


def start_of_week(date, min_date):
    days_difference = (date - min_date).days
    start_week_date = min_date + timedelta(weeks=(days_difference // 7))
    return start_week_date


# Dictionary to count users for each start of the week
weekly_counts = {}

# Process each user to count the start of the week
for user in users:
    week_start = start_of_week(user['createdDate'], min_date)
    if week_start not in weekly_counts:
        weekly_counts[week_start] = 0
    weekly_counts[week_start] += 1

# Create a DataFrame from the weekly counts
df = pd.DataFrame(list(weekly_counts.items()),
                  columns=['Week Start', 'User Count'])

# Sort DataFrame by Week Start
df.sort_values('Week Start', inplace=True)

# Output to Excel
excel_file = 'user_weekly_counts.xlsx'
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"User counts by week start have been written to {excel_file}.")
