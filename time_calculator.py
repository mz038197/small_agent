import datetime

def calculate_time_difference(start_time, end_time):
    format = '%Y-%m-%d %H:%M:%S'
    start = datetime.datetime.strptime(start_time, format)
    end = datetime.datetime.strptime(end_time, format)
    return end - start

if __name__ == '__main__':
    start_time = '2023-10-01 12:00:00'
    end_time = '2023-10-01 15:30:00'
    time_difference = calculate_time_difference(start_time, end_time)
    print(f'時間差: {time_difference}')