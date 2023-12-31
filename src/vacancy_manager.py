import json
from abc import ABC, abstractmethod
from typing import List

from src.vacancy import Vacancy

import os


class VacancyManager(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy_obj: Vacancy):
        """
        Абстрактный метод для добавления вакансии.

        :param vacancy_obj: Объект вакансии для добавления.
        """
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        """
        Абстрактный метод для получения списка вакансий.

        :return: Список вакансий.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_obj: Vacancy):
        """
        Абстрактный метод для удаления вакансии.

        :param vacancy_obj: Объект вакансии для удаления.
        """
        pass

    @abstractmethod
    def filter_vacancies(self, params: List[str]) -> List[Vacancy]:
        """
        Абстрактный метод для фильтрации вакансий.

        :param params: Список ключевых слов для фильтрации.
        :return: Отфильтрованный список вакансий.
        """
        pass


class JSONSaver(VacancyManager):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(current_directory, "store", "vacancies.json")

    def __init__(self):
        self.vacancies: List[Vacancy] = []

    def check_file_exists(self):
        if not os.path.exists(self.file_path) or not os.path.getsize(self.file_path):
            raise FileNotFoundError('Файл с вакансиями пуст или не существует.')

    def add_vacancy(self, vacancy_obj: Vacancy):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path):
            with open(self.file_path, encoding='utf8') as file:
                vc_list = json.load(file)
        else:
            vc_list = []

        vc_list.append(vacancy_obj)

        with open(self.file_path, 'w', encoding='utf8') as file:
            json.dump(vc_list, file, ensure_ascii=False)

    def get_vacancies(self) -> List[Vacancy]:
        self.check_file_exists()

        with open(self.file_path, encoding='utf8') as file:
            vc_list = json.load(file)

            self.vacancies = [Vacancy(vc) for vc in vc_list]
            return self.vacancies

    def filter_vacancies(self, params: List[str]) -> List[Vacancy]:
        if params is None:
            raise ValueError('Необходимо указать ключевое слово для поиска.')
        if len(params) == 0:
            raise ValueError('Фильтрация пробела недопустима.')

        params_lower = [param.lower() if isinstance(param, str) else param for param in params]

        filtered_vacancies = []

        for vc in self.vacancies:
            vc_attrs = [vc.name.lower(), vc.experience.lower(), str(vc.salary_from), str(vc.salary_to)]
            if any(param in attr for param in params_lower for attr in vc_attrs):
                filtered_vacancies.append(vc)

        self.vacancies = filtered_vacancies
        return self.vacancies

    def sort_vacancies_by_salary(self) -> List[Vacancy]:
        sorted_vacancies = sorted(self.vacancies, key=lambda vc: max(vc.salary_from or 0, vc.salary_to or 0))

        self.vacancies = sorted_vacancies
        return self.vacancies

    def delete_vacancy(self, vacancy_obj: Vacancy):
        if vacancy_obj is None:
            raise ValueError('Необходимо указать вакансию для удаления')

        self.check_file_exists()

        with open(self.file_path, encoding='utf8') as file:
            vc_list = json.load(file)
            vc_list_cleared = []

            for vacancy in vc_list:
                if vacancy['url'].lower() != vacancy_obj.url.lower():
                    vc_list_cleared.append(vacancy)

        with open(self.file_path, 'w', encoding='utf8') as file:
            json.dump(vc_list_cleared, file, ensure_ascii=False)
