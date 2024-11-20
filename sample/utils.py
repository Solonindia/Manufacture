from datetime import time, datetime, timedelta

def get_time_intervals():
    intervals = []
    start_time = time(8, 0)  # 8:00 AM
    end_time = time(23, 59)  # 12:00 AM (midnight)
    
    while start_time <= end_time:  # inclusive of end time
        intervals.append(start_time.strftime('%I:%M %p'))
        start_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=1)).time()  # increment by 1 hour
    
    return intervals
