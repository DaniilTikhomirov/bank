from datetime import datetime


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
