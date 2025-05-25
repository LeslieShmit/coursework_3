from abc import ABC, abstractmethod

import requests
from mypy.types_utils import AnyType


class Parser(ABC):
    """Абстрактный класс для работы с API сервисом"""

    @abstractmethod
    def _connect_to_api(self, keyword:str):
        """Абстрактный метод для подключения к API"""
        pass

    @abstractmethod
    def load_vacancies(self, keyword:str):
        """Абстрактный метод для получения вакансий по ключевому слову"""
        pass


class HH(Parser):
    """Класс для работы с API hh.ru"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"

    def _connect_to_api(self, keyword: str) -> list[dict] | None:
        """Приватная функция подключения к API"""
        params = {"employer_id": keyword, "per_page": 20}
        response = requests.get(self.__url, params=params)
        if response.status_code != 200:
            print(f"Ошибка при обработке запроса: {response.status_code}")
            return None
        data = response.json()
        return data

    def load_vacancies(self, keyword:str="") -> list[AnyType]:
        """Функция получает вакансии по id работодателя"""
        data = self._connect_to_api(keyword)
        if data and "items" in data:
            return data["items"]
        else:
            return []
