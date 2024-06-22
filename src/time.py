from datetime import datetime, timedelta


def find_time_of_day(date: str) -> str:
    date_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%H")
    if 4 <= int(date_object) <= 11:
        return "Доброе утро"
    elif 12 <= int(date_object) <= 16:
        return "Добрый день"
    elif 17 <= int(date_object) <= 23:
        return "Добрый вечер"
    elif 0 <= int(date_object) <= 3:
        return "Доброй ночи"
    return "Добро пожаловать"


def range_time(date: str, week: int) -> list:
    base = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    b1 = int(base.strftime("%m")) - week
    b = 13
    date_list = []
    while b != b1:
        date_list.append(base.strftime("%m %d %Y"))
        base = base - timedelta(days=1)
        b = int(base.strftime("%m"))
    return date_list


def find_range_time(operation: list[dict], date_list: list) -> list[dict]:
    new_list = []
    for item in operation:
        if item["Дата платежа"]:
            date = datetime.strptime(item["Дата платежа"], "%d.%m.%Y").strftime("%m %d %Y")
            if date in date_list:
                new_list.append(item)
    return new_list
