import json
import os.path
from typing import Any
import pandas as pd
import requests

from src.config_log import setting_log

logger = setting_log(__name__)


def unpack_json(path: str) -> Any:
    """
    открывает json файл
    :param path: путь к файлу
    :return: переобразованный json файл в list[dict] или пустой список
    """
    try:
        with open(os.path.relpath(path), "r", encoding="utf8") as file:
            logger.info("search file...")
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                logger.info("error decode")
                return []
            else:
                logger.info("unpack file")
                return data
    except FileNotFoundError:
        logger.info("not found file")
        return []


def write_xml_from_web(url: str, name: str) -> None:
    """
    записывает xml файл с сайта
    :param url:ссылка на сайт
    :param name:имя файла
    :return: None
    """
    req = requests.get(url)
    logger.info("get request")
    with open(os.path.join("..", "data", f"{name}.xml"), "wb") as file:
        logger.info("write xml file")
        file.write(req.content)


def unpack_csv(path: str) -> list:
    """распоковывает cvs"""
    logger.info("unpacking csv...")
    csv_file = pd.read_csv(path, encoding="utf-8", sep=";")
    json_csv = csv_file.to_dict(orient="records")
    logger.info("unpack")
    return json_csv


def unpack_excel(path: str) -> list:
    """распоковывает exel"""
    logger.info("unpacking excel...")
    formating_excel = pd.read_excel(path, na_filter=False)
    json_excel = formating_excel.to_dict(orient="records")
    logger.info("unpack")
    return json_excel
