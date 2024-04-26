import os
from typing import Any


class Depiction:
    def __init__(self, data: dict[str, Any]):
        self.link = data.get('@id')
        self.title = data.get('title')
        self.license = data.get('license')
        self.url = data.get('url')

    def __repr__(self) -> str:
        return str(self.__dict__)
