from config import prodtimings_collection
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from pprint import pprint

schedules = list(prodtimings_collection.find(
    {"expert": ObjectId("66046a3d42f04a057fa21034")}))


# Function to get available time slots
def get_available_time_slots(day):
    # Find the schedule for the specified day
    schedule = next(
        (s for s in schedules if s['day'].lower() == day.lower()), None)

    if not schedule:
        print(f"No schedule found for {day}")
        return

    # Function to generate time slots
    def generate_slots(start_time_str, end_time_str):
        start_time = datetime.strptime(start_time_str, '%H:%M')
        end_time = datetime.strptime(end_time_str, '%H:%M')
        slots = []

        current_time = start_time
        while current_time + timedelta(minutes=30) <= end_time:
            end_slot_time = current_time + timedelta(minutes=30)
            slots.append(f"{current_time.strftime(
                '%H:%M')} - {end_slot_time.strftime('%H:%M')}")
            current_time = end_slot_time

        return slots

    # Generate slots for primary time
    primary_slots = generate_slots(
        schedule['PrimaryStartTime'], schedule['PrimaryEndTime'])

    # Generate slots for secondary time, if available
    secondary_slots = []
    if 'SecondaryStartTime' in schedule and 'SecondaryEndTime' in schedule:
        secondary_slots = generate_slots(
            schedule['SecondaryStartTime'], schedule['SecondaryEndTime'])

    # Combine primary and secondary slots
    all_slots = primary_slots + secondary_slots

    return all_slots


# Example usage: Get available time slots for a given day
user_selected_day = 'Monday'  # Change this to any day you want
slots = get_available_time_slots(user_selected_day)

print(f"Available time slots for {user_selected_day}:")
pprint(slots)
