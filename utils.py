from datetime import datetime, timedelta

def format_timestamp(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time
    
def is_recent(timestamp):
    current_time = datetime.now()
    five_minutes_ago = current_time - timedelta(minutes=3)
    return datetime.fromtimestamp(timestamp) > five_minutes_ago

def is_in_blacklist(url):
    with open('blacklists.txt', 'r', encoding='utf-8') as f:
        black_list = f.read().splitlines()
    return any(substring in url for substring in black_list)

def format_number(number, sig_figs=3):
    suffixes = ['', 'k', 'M', 'B', 'T']
    idx = 0

    while abs(number) >= 1000 and idx < len(suffixes) - 1:
        idx += 1
        number /= 1000.0
    rounded_number = round(number, sig_figs - 1)
    formatted_number = f"{rounded_number:.{sig_figs}g}"
    return f"{formatted_number}{suffixes[idx]}"
