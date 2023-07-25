from typing import Union


class Vacancy:
    __slots__ = ("__name", "__experience", "__salary_from", "__salary_to", "__currency", "__employer", "__url")

    def __init__(self, vc_obj):
        self.__name = self.__validate_value(vc_obj["name"])
        self.__experience = self.__validate_value(vc_obj["experience"])
        self.__salary_from = self.__validate_value(vc_obj["salary_from"])
        self.__salary_to = self.__validate_value(vc_obj["salary_to"])
        self.__currency = self.__validate_value(vc_obj["currency"])
        self.__employer = self.__validate_value(vc_obj["employer"])
        self.__url = self.__validate_value(vc_obj["url"])

    @staticmethod
    def __validate_value(value):
        return "" if value is None else value

    @staticmethod
    def __check_compare(other, _object):
        if not isinstance(other, _object):
            raise TypeError(f"Невозможно сравнить объект типа '{_object}' с объектом другого типа.")

    @property
    def employer(self) -> str:
        return self.__employer

    @property
    def currency(self) -> str:
        return self.__currency

    @property
    def experience(self) -> str:
        return self.__experience

    @property
    def salary_to(self) -> str:
        return self.__salary_to

    @property
    def name(self) -> str:
        return self.__name

    @property
    def url(self) -> str:
        return self.__url

    @salary_to.setter
    def salary_to(self, value):
        self.__salary_to = self.__validate_value(value)

    @property
    def salary_from(self) -> str:
        return self.__salary_from

    @salary_from.setter
    def salary_from(self, value):
        self.__salary_from = self.__validate_value(value)

    @property
    def get_salary_range(self) -> int:
        """
        Максимальное значение зарплаты
        :return: Возврат максимального значения зарплаты
        """
        return max(self.__salary_from, self.__salary_to)

    def __str__(self) -> str:
        salary_range = f"{self.salary_from} - {self.salary_to} {self.currency}" \
            if self.salary_from and self.salary_to else "Не указана"
        return f"Вакансия: {self.name}\n" \
               f"Зарплата: {salary_range}\n" \
               f"Требуемый опыт: {self.experience}\n" \
               f"Ссылка: {self.url}\n" \
               f"Работодатель: {self.employer}\n"

    def __lt__(self, other) -> bool:
        """
        Сравнение по оператору 'меньше'
        :param other: Экземпляр класса
        :return: Возврат булевого значения
        """
        self.__check_compare(other, Vacancy)
        return self.get_salary_range < other.get_salary_range

    def __gt__(self, other) -> bool:
        """
        Сравнение по оператору 'больше'
        :param other: Экземпляр класса
        :return: Возврат булевого значения
        """
        self.__check_compare(other, Vacancy)
        return self.get_salary_range > other.get_salary_range

    def __eq__(self, other) -> bool:
        """
        Сравнение по оператору 'равенства'
        :param other: Экземпляр класса
        :return: Возврат булевого значения
        """
        self.__check_compare(other, Vacancy)
        return self.get_salary_range == other.get_salary_range
