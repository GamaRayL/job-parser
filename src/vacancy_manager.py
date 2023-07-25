import json
from abc import ABC, abstractmethod

from src.vacancy import Vacancy

import os


class VacancyManager(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy_obj):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_obj):
        pass

    @abstractmethod
    def filter_vacancies(self, params):
        pass


class JSONSaver(VacancyManager):
    dir = './store/'
    filename = 'vacancy.json'
    path = dir + filename

    def __init__(self):
        self.vacancies = []

    def check_file_exists(self):
        if not os.path.exists(self.path) or not os.path.getsize(self.path):
            raise FileNotFoundError('Файл с вакансиями пуст или не существует.')

    def add_vacancy(self, vacancy_obj):
        if os.path.exists(self.path) and os.path.getsize(self.path):
            with open(self.path, encoding='utf8') as file:
                vc_list = json.load(file)
        else:
            vc_list = []

        vc_list.append(vacancy_obj)

        with open(self.path, 'w', encoding='utf8') as file:
            json.dump(vc_list, file, ensure_ascii=False)

    def get_vacancies(self):
        self.check_file_exists()

        with open(self.path, encoding='utf8') as file:
            vc_list = json.load(file)

            self.vacancies = [Vacancy(vc) for vc in vc_list]
            return self.vacancies

    def filter_vacancies(self, params):
        if params is None:
            raise ValueError('Необходимо указать ключевое слово для поиска.')
        if len(params) == 0:
            raise ValueError('Фильтрация пробела недопустима.')

        params_lower = [param.lower() if isinstance(param, str) else param for param in params]

        vacancies = []

        for vc in self.vacancies:
            vc_attrs = [vc.name.lower(), vc.experience.lower(), str(vc.salary_from), str(vc.salary_to)]
            if any(param in attr for param in params_lower for attr in vc_attrs):
                vacancies.append(vc)

        self.vacancies = vacancies
        return self.vacancies

    def sort_vacancies_by_salary(self):
        sorted_vacancies = sorted(self.vacancies, key=lambda vc: max(vc.salary_from or 0, vc.salary_to or 0))
        return sorted_vacancies

    def delete_vacancy(self, vacancy_obj):
        if vacancy_obj is None:
            raise ValueError('Необходимо указать вакансию для удаления')

        self.check_file_exists()

        with open(self.path, encoding='utf8') as file:
            vc_list = json.load(file)
            vc_list_cleared = []

            for vacancy in vc_list:
                if vacancy['url'].lower() != vacancy_obj.url.lower():
                    vc_list_cleared.append(vacancy)

        with open(self.path, 'w', encoding='utf8') as file:
            json.dump(vc_list_cleared, file, ensure_ascii=False)
