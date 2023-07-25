import math
from abc import ABC, abstractmethod
import requests

from src.exceptions import ParsingError


class VacancyEngine(ABC):
    """Абстрактный класс для работы с API сайтов вакансий"""

    @abstractmethod
    def get_request(self):
        """
        Получения списка вакансий
        :return: Коллекция со списком вакансий
        """
        pass

    @abstractmethod
    def get_vacancies(self):
        """
        Получение вакансий с использованием API.
        """
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        """
        Получение отформатированных данных о вакансиях.
        """
        pass


class HeadHunterAPI(VacancyEngine):
    url = f"https://api.hh.ru/vacancies"

    def __init__(self, keyword):
        self.quantity = None
        self.vacancies = []
        self.params = {
            "page": 1,
            "per_page": 100,
            "text": keyword,
            "archived": False
        }

    def get_request(self):
        response = requests.get(self.url, params=self.params)

        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус {response.status_code}")

        return response.json()["items"]

    def get_vacancies(self, quantity: int = 400):
        pages_count = math.ceil(quantity / self.params["per_page"])
        self.quantity = quantity
        self.vacancies = []

        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")

            try:
                self.params["per_page"] = self.quantity if self.quantity < 100 else 100
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                self.quantity -= self.params["per_page"]
                print(f"Загружено вакансий: {len(page_vacancies)}. Успех!")
            if len(page_vacancies) == 0:
                break

    def get_formatted_vacancies(self):
        formatted_vacancies = []

        for vacancy in self.vacancies:
            salary = vacancy["salary"]

            formatted_vacancy = {
                "name": vacancy["name"],
                "experience": vacancy["experience"]["name"],
                "salary_from": salary["from"] if salary and salary["from"] != 0 else None,
                "salary_to": salary["to"] if salary and salary["to"] != 0 else None,
                "currency": salary["currency"] if salary and salary["currency"] else None,
                "employer": vacancy["employer"]["name"],
                "url": vacancy["alternate_url"],
            }
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies


class SuperJobAPI(VacancyEngine):
    url = f'https://api.superjob.ru/2.0/vacancies'

    def __init__(self, keyword):
        self.quantity = None
        self.vacancies = []

        self.params = {
            "page": None,
            "count": 100,
            "keyword": keyword,
            "archive": False
        }
        self.headers = {
            'X-Api-App-Id': 'v3.r.137691624.07e3b025a9ab43ea2c2d4d2f90631ce447940fff'
                            '.b2a761e6fcefbbd35597ca97eca35fe0b7d2b71a'
        }

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)

        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус {response.status_code}")

        return response.json()["objects"]

    def get_vacancies(self, quantity: int = 400):
        pages_count = math.ceil(quantity / self.params["count"])
        self.quantity = quantity
        self.params["count"] = quantity if quantity < 100 else 100
        self.vacancies = []

        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")

            try:
                self.params["count"] = self.quantity if self.quantity < 100 else 100
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                self.quantity -= self.params["count"]
                print(f"Загружено вакансий: {len(page_vacancies)}. Успех!")
            if len(page_vacancies) == 0:
                break

    def get_formatted_vacancies(self):
        formatted_vacancies = []

        for vacancy in self.vacancies:
            formatted_vacancy = {
                "name": vacancy["profession"],
                "experience": vacancy["experience"]["title"],
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] != 0 else None,
                "currency": vacancy["currency"],
                "employer": vacancy["firm_name"],
                "url": vacancy["link"],
            }
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies
