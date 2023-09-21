import os
from bs4 import BeautifulSoup
import requests

class DataScrapper:
    url : str
    headers: dict

    _data: BeautifulSoup

    def __init__(self, url: str, header:dict=None ) -> None:
        self.url = url
        self.headers = header

    def pull_from_file_or_url(self, path: str) -> BeautifulSoup:
        if os.path.isfile(path):
            return self.pull_from_file(path)
        return self.pull()

    def pull(self) -> BeautifulSoup:
        request = requests.get(self.url, self.headers)
        self._data = BeautifulSoup(request.content, "html.parser")
        return self._data 

    def pull_from_file(self, path: str) -> BeautifulSoup:
        with open(path, "r", encoding="utf-8") as file:
            source = file.read()

        self._data = BeautifulSoup(source, "html.parser")
        return self._data

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as file:
            file.write(str(self._data.prettify()))

