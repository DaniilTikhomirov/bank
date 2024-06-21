from decimal import Decimal
from src.utils import unpack_excel
from datetime import datetime, timedelta


def info_from_operation(operation: list[dict]) -> list[dict]:
    """
    находит общую сумму всех операция по каждой карте
    :param operation: данные операций
    :return: список с словорями с информацией о операциях по каждой карте
    """
    info_card: dict = {}
    for item in operation:
        if int(item['Сумма операции']) < 0:
            name = item['Номер карты']

            if len(name) >= 4:
                name = name[-4:]
                sum_operation = (info_card.get(name, {}).get('total_spent', 0)) + (
                        Decimal(str(item['Сумма операции'])) * -1)
                sum_cashback = int(sum_operation) // 100
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

    list_info = []
    for k, v in info_card.items():
        list_info.append(
            {'last_digits': k, 'total_spent': info_card[k]['total_spent'], 'cashback': info_card[k]['cashback']})
    return list_info


def find_top_transactions(operation: list[dict], top: int = 5) -> list[dict]:
    top_list = []
    operation = list(filter(lambda x: int(x['Сумма операции']) < 0, operation))
    for _ in range(top):
        leader = operation.pop(operation.index(max(operation, key=lambda x: x['Сумма операции'] * -1)))
        top_list.append({'date': leader['Дата платежа'],
                         'amount': float(leader['Сумма операции']) * -1,
                         'category': leader['Категория'],
                         'description': leader['Описание']})
    return top_list


data = unpack_excel("..\\data\\operations.xls")

print(*info_from_operation(data), sep='\n')
print()
print(*find_top_transactions(data), sep='\n')
print()
base = datetime.today()
b1 = base.strftime('%m')
b = 65
date_list = []
print(b)
while int(b) != (int(b1) - 1):
    print(int(b) - 1)
    date_list.append(base.strftime('%m %d'))
    base = base - timedelta(days=1)
    b = base.strftime('%m')
print(date_list)