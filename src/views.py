import os
import json
from src.time import find_time_of_day
from src.operation import info_from_operation, find_top_transactions
from src.currency import get_currencies, get_sp500
from src.utils import unpack_excel
from src.config_log import setting_log

loger = setting_log('views')


def major(date: str):
    """
    возврощает Json-ответ с информацией на главной
    :param date: дата
    :return: возврощает json-ответ
    """
    with open(os.path.join("..", "user_settings.json")) as f:
        loger.info('loading_json...')
        info = json.load(f)
    loger.info('get greeting...')
    greeting = find_time_of_day(date)
    list_currency = info["user_currencies"]
    list_stocks = info["user_stocks"]
    loger.info('get data...')
    data = unpack_excel(os.path.join("..", "data", "operation.xls"))
    loger.info('load operation..')
    list_operation = info_from_operation(data, date)
    loger.info('load top...')
    top = find_top_transactions(data, date)
    loger.info('load currecies...')
    currency = get_currencies(list_currency)
    loger.info('get sp500...')
    sp500 = get_sp500(list_stocks)
    json_file = {"greeting": greeting,
            "cards": list_operation,
            "top_transactions": top,
            "currency_rates": currency,
            "stock_prices": sp500
            }
    return json.dumps(json_file)


