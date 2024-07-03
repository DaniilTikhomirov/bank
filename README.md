
# Приложение для анализа банковских операций

Анализирует банковские операции с Excel у пользователя.


# Веб-страницы

##  Главная
_принемает на вход строку с датой и временем в формате_
YYYY-MM-DD HH:MM:SS
 _и возвращающую JSON-ответ со следующими данными:_

_Приветствие в формате_ 
"???"
, где 
???
 — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» _в зависимости от текущего времени._
_По каждой карте:
последние 4 цифры карты;
общая сумма расходов;
кешбэк (1 рубль на каждые 100 рублей).
Топ-5 транзакций по сумме платежа.
Курс валют.
Стоимость акций из S&P500._
***
```python  
def major(date: str) -> str:
    """
    возврощает Json-ответ с информацией на главной
    :param date: дата
    :return: возврощает json-ответ
    """
    with open(os.path.join(Path(__file__).resolve().parents[1], "user_settings.json")) as f:
        loger.info("loading_json...")
        info = json.load(f)
    loger.info("get greeting...")
    greeting = find_time_of_day(date)
    list_currency = info["user_currencies"]
    list_stocks = info["user_stocks"]
    loger.info("get data...")
    data = unpack_excel(os.path.join(Path(__file__).resolve().parents[1], "data", "operation.xls"))
    loger.info("load operation..")
    list_operation = info_from_operation(data, date)
    loger.info("load top...")
    top = find_top_transactions(data, date)
    loger.info("load currecies...")
    currency = get_currencies(list_currency)
    loger.info("get sp500...")
    sp500 = get_sp500(list_stocks)
    json_file = {
        "greeting": greeting,
        "cards": list_operation,
        "top_transactions": top,
        "currency_rates": currency,
        "stock_prices": sp500,
    }
    return json.dumps(json_file, ensure_ascii=False)
```
---
#### функция находится в service.py

#### все вспомогательные функции импортировны из модулей currency.py, operation.py, time.py, utils.py 

# Сервисы

##  Простой поиск
_Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории_
***
```python  
def simple_find(line: str) -> Any:
    """ищет операции с заданной категорией"""
    try:
        logger.info("starting...")
        file = unpack_excel(os.path.join("..", "data", "operation.xls"))
        logger.info("file ready")
        json_file = json.dumps(find_line(file, line), ensure_ascii=False)
        logger.info("dumps ready")
        return json_file
    except Exception as error:
        logger.error(f"error:{error}")
        raise error
```
---
#### функция находится в service.py

#### все вспомогательные функции импортировны из модулей operation.py, utils.py 

# Отчеты

##  Траты по категории
_Функция принимает на вход:_

_датафрейм с транзакциями,
название категории,
опциональную дату.
Если дата не передана, то берется текущая дата._

_Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)._
***
```python  
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    возвращает траты по заданной категории за последние три месяца от переданной даты
    :param transactions: датафрейм операций
    :param category: категория
    :param date: дата если дата не подается то берется текушая
    :return: возврощает датафрейм
    """
    try:
        transactions = transactions[transactions["Сумма платежа"] < 0]
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"get now time: {date}")
        list_time = range_time(date, 3)
        logger.info("find category...")
        transactions = find_category_df(transactions, category)
        logger.info("find time range...")
        transactions = find_range_time_df(transactions, list_time)
        logger.info("done")
        return transactions
    except Exception as error:
        logger.error(f"error:{error}")
        raise error
```
---
#### функция находится в reports.py

#### все вспомогательные функции импортировны из модулей operation.py, time.py 


## Appendix

пособно обрабатывать банковские операции и возвращать сумму транзакций и кэшбэк по каждой карте. Также оно может предоставлять топ 5 операций и стоимость ваших валют и акций S&P 500. Помимо этого, приложение имеет возможность искать операции в диапазоне до 3 месяцев по заданной категории


## Environment Variables

Чтобы запустить этот проект, вам нужно будет добавить следующие переменные среды в ваш env-файл

`API`



## Authors

- [@DaniilTikhomirov](https://www.github.com/DaniilTikhomirov)

