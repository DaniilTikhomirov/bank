from datetime import datetime, timedelta


def find_time_of_day(date: str) -> str:
    date_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%H')
    if 4 <= int(date_object) <= 11:
        return "Доброе утро"
    elif 12 <= int(date_object) <= 16:
        return "Добрый день"
    elif 17 <= int(date_object) <= 23:
        return "Добрый вечер"
    elif 0 <= int(date_object) <= 3:
        return "Доброй ночи"
    return "Добро пожаловать"


def range_time():
    base = datetime.today()
    b1 = base.strftime('%m')
    b = 65
    date_list = []
    while int(b) != (int(b1) - 1):
        date_list.append(base.strftime('%m %d'))
        base = base - timedelta(days=1)
        b = base.strftime('%m')
    return date_list