

duration = 1226


def seconds_to_duration_str() -> str:
    seconds = int(duration)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{hours:02}:{minutes:02}:{seconds:02}'


print(seconds_to_duration_str())
