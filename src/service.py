import json
import os.path
from typing import Any

from src.operation import find_line
from src.utils import unpack_excel


def simple_find(line: str) -> Any:
    file = unpack_excel(os.path.join('..', 'data', 'operation.xls'))
    return json.dumps(find_line(file, line), ensure_ascii=False)
