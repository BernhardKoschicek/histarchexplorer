from typing import Any

import requests

from histarchexplorer import app
from histarchexplorer.api.parser import Parser

PROXIES = {
    "http": app.config['API_PROXY'],
    "https": app.config['API_PROXY']}


class ApiAccess:

    @staticmethod
    def get_entity(id_: int, parser: Parser) -> dict[str, Any]:
        req = requests.get(
            f"{app.config['API_URL']}entity/{id_}",
            params=parser.__dict__,
            proxies=PROXIES,
            timeout=60).json()
        return req

    @staticmethod
    def get_by_system_class(
            class_: str,
            parser: Parser) -> list[dict[str, Any]]:
        print(parser.__dict__)
        req = requests.get(
            f"{app.config['API_URL']}system_class/{class_}",
            params=parser.__dict__,
            proxies=PROXIES,
            timeout=60).json()
        return req['results']
