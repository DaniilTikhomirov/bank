from decimal import Decimal
from src.utils import unpack_excel
from datetime import datetime, timedelta
from src.time import range_time, find_range_time


def info_from_operation(operation: list[dict], date: str) -> list[dict]:
    """
    находит общую сумму всех операция по каждой карте
    :param operation: данные операций
    :param date дата от которой идет отсчет
    :return: список с словорями с информацией о операциях по каждой карте
    """
    operation = find_range_time(operation, range_time(date, 1))
    info_card: dict = {}
    for item in operation:
        # берем только траты
        if int(item['Сумма операции']) < 0:
            if operation:
                name = item['Номер карты']
                # проверяем указана ли карта
                if len(name) >= 4:
                    name = name[-4:]
                    sum_operation = (info_card.get(name, {}).get('total_spent', 0)) + (
                            Decimal(str(item['Сумма операции'])) * -1)
                    sum_cashback = sum_operation / 100
                    info_card[name] = {
                        'total_spent': sum_operation,
                        'cashback': sum_cashback}

                else:
                    name = 'Переводы'
                    sum_operation = (info_card.get(name, {}).get('total_spent', 0)) + (
                            Decimal(str(item['Сумма операции'])) * -1)
                    info_card['Переводы'] = {
                        'total_spent': sum_operation,
                        'cashback': 0}
    # формируем список
    list_info = []
    for k, v in info_card.items():
        list_info.append(
            {'last_digits': k, 'total_spent': info_card[k]['total_spent'], 'cashback': info_card[k]['cashback']})
    return list_info


def find_top_transactions(operation: list[dict], date: str, top: int = 5) -> list[dict]:
    """
    находит топ транзакий в диапозоне даты
    :param operation данные операций
    :param date дата
    :param top число топов
    :return список с топом операций
    """
    top_list = []
    # берем только траты
    operation = list(filter(lambda x: int(x['Сумма операции']) < 0, operation))
    operation = find_range_time(operation, range_time(date, 1))
    # проверка на топ
    if top > len(operation):
        top = len(operation)
    # находим топ
    for _ in range(top):
        if operation:
            leader = operation.pop(operation.index(max(operation, key=lambda x: x['Сумма операции'] * -1)))
            top_list.append({'date': leader['Дата платежа'],
                             'amount': float(leader['Сумма операции']) * -1,
                             'category': leader['Категория'],
                             'description': leader['Описание']})
    return top_list


data = unpack_excel("..\\data\\operation.xls")
date1 = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

print(*info_from_operation(data, date1), sep='\n')
print()
print(*find_top_transactions(data, date1, ), sep='\n')
