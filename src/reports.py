from datetime import datetime
from typing import Optional

import pandas as pd
from src.time import find_range_time_df, range_time
from src.operation import find_category_df
from src.config_log import setting_log

logger = setting_log('reports')


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    возвращает траты по заданной категории за последние три месяца от переданной даты
    :param transactions: датафрейм операций
    :param category: категория
    :param date: дата если дата не подается то берется текушая
    :return: возврощает датафрейм
    """
    try:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f'get now time: {date}')
        list_time = range_time(date, 3)
        logger.info('find category...')
        transactions = find_category_df(transactions, category)
        logger.info("find time range...")
        transactions = find_range_time_df(transactions, list_time)
        logger.info('done')
        return transactions
    except Exception as error:
        logger.error(f'error:{error}')
        raise error
