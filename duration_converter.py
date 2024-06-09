from config import devcalls_collection

calls = list(devcalls_collection.find())


def convert_duration(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    return hours * 3600 + minutes * 60 + seconds


durations = []

total_calls = len(calls)
for index, call in enumerate(calls):
    if "durationInSeconds" in call or "duration" not in call or call["duration"] == "":
        continue
    call_duration = call["duration"]
    formatted_duration = convert_duration(call_duration)
    # calls_collection.update_one(
    #     {"callId": call["callId"]}, {"$set": {"durationInSeconds": formatted_duration}}
    # )
    durations.append(formatted_duration)
    percentage = (index + 1) / total_calls * 100
    print(f"Progress: {percentage:.2f}%")

print(f"Total Duration: {sum(durations)}")
print(f"Average duration: {sum(durations) / len(durations)}")
