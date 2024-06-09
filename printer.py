from config import prodcalls_collection, prodschedules_collection

calls = prodcalls_collection.count_documents({"type": "scheduled"})
schedules = prodschedules_collection.count_documents({})
successful_schedules = prodschedules_collection.count_documents({"status": "successful"})
print(f"Total number of schedules: {schedules}")
print(f"Total number of successful schedules: {successful_schedules}")
print(f"Total number of scheduled calls: {calls}")
