import os.path
import xml.etree.ElementTree as ET
from datetime import datetime
from decimal import Decimal

from src.config_log import setting_log
from src.utils import write_xml_from_web

logger = setting_log(__name__)

# словарь код валюты: ID валюты
CODE_CURRENCY = {
    "AUD": "R01010",
    "AZN": "R01020A",
    "GBP": "R01035",
    "AMD": "R01060",
    "BYN": "R01090B",
    "BGN": "R01100",
    "BRL": "R01115",
    "HUF": "R01135",
    "VND": "R01150",
    "HKD": "R01200",
    "GEL": "R01210",
    "DKK": "R01215",
    "AED": "R01230",
    "USD": "R01235",
    "EUR": "R01239",
    "EGP": "R01240",
    "INR": "R01270",
    "IDR": "R01280",
    "KZT": "R01335",
    "CAD": "R01350",
    "QAR": "R01355",
    "KGS": "R01370",
    "CNY": "R01375",
    "MDL": "R01500",
    "NZD": "R01530",
    "NOK": "R01535",
    "PLN": "R01565",
    "RON": "R01585F",
    "XDR": "R01589",
    "SGD": "R01625",
    "TJS": "R01670",
    "THB": "R01675",
    "TRY": "R01700J",
    "TMT": "R01710A",
    "UZS": "R01717",
    "UAH": "R01720",
    "CZK": "R01760",
    "SEK": "R01770",
    "CHF": "R01775",
    "RSD": "R01805F",
    "ZAR": "R01810",
    "KRW": "R01815",
    "JPY": "R01820",
}


def get_currencies(currency: str) -> Decimal | bool:
    """
    находит в xml файле цену этой валюты в рублях
    :param currency: валюта
    :return: цена валюты
    """
    if currency == "RUB":
        logger.info("currency is RUB")
        return Decimal("1")
    # получает актуальную дату
    time_now = datetime.strftime(datetime.now(), "%d/%m/%Y")
    # использую дату как ссылку для xml данных центра банка
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={time_now}"
    # функция которая записывает xml с айта
    write_xml_from_web(url, "cbr")
    # парсим данные с нашего файла
    logger.info("parse data...")
    three = ET.parse(os.path.join("..", "data", "cbr.xml"))
    # получаем корневой элемент
    root = three.getroot()
    # проходимся по корню`
    for child in root:
        if child.attrib["ID"] == CODE_CURRENCY[currency]:
            element = child.find("Value")
            if element is not None:
                value = element.text
                value_currency = Decimal(str(value).replace(",", "."))
                logger.info(f"good parse value is {str(value_currency)}")
                return value_currency
            else:
                logger.info("bad parse")
                return False
    return Decimal("0")


def calculate_amount_in_rub(operation: dict) -> Decimal | str:
    """
    считает сумму операции в рублях
    :param operation: операция
    :return: сумма операции в рублях
    """
    code_currency = operation["operationAmount"]["currency"]["code"]
    amount = operation["operationAmount"]["amount"]
    currency = get_currencies(code_currency)
    logger.info("calculate...")
    if currency:
        amount_in_rub = Decimal(amount) * currency
        logger.info(f"calculate {amount_in_rub}")
        return amount_in_rub
    logger.info("error parsing")
    return "error parsing"
