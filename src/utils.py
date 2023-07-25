from typing import Dict

from src.vacancy_api import HeadHunterAPI, SuperJobAPI
from src.vacancy_manager import JSONSaver


def select_variant(message: str, variants: Dict[int, str]) -> int:
    """
    Отображает сообщение с вариантами и получает выбор пользователя.

    :param message: Сообщение для отображения.
    :param variants: Словарь с номерами вариантов и соответствующими им описаниями.
    :return: Выбранный номер варианта.
    """

    while True:
        print(message)

        for prop, value in variants.items():
            print(f"{prop}. {value}.")

        try:
            variant_choose = int(input())
        except ValueError:
            print("Введите числовое значение!\n")
            continue

        if variant_choose in variants:
            return variant_choose
        else:
            print(
                f"Ваш выбор '{variant_choose}' не подходит под правильный вариант"
                f" ({[prop for prop in variants.items()]})!\n")
            continue


def user_interaction():
    """
    Функция для взаимодействия с пользователем по поиску работы, фильтрации и сортировке вакансий.
    """
    print("Добро пожаловать в программу для поиска вакансий!\n")

    # Выбор платформы
    platform_message = "Выберите пожалуйста платформу для поиска (указав цифру):"
    platforms = {
        1: "HeadHunter",
        2: "SuperJob",
        3: "На всех платформах",
        4: "Завершить программу"
    }
    select_platform = select_variant(platform_message, platforms)
    print(f"Для поиска выбрана платформа '{platforms[select_platform]}'\n")

    if select_platform == 4:
        return

    vacancies = []
    search_query = input("Введите поисковый запрос: ")
    n_vc_query = int(input("Введите количество вакансий в запросе: "))

    hh = HeadHunterAPI(search_query)
    superjob = SuperJobAPI(search_query)

    if select_platform == 1:
        hh.get_vacancies(n_vc_query)
        vacancies.extend(hh.get_formatted_vacancies())
    elif select_platform == 2:
        superjob.get_vacancies(n_vc_query)
        vacancies.extend(superjob.get_formatted_vacancies())
    elif select_platform == 3:
        hh.get_vacancies(n_vc_query // 2)
        superjob.get_vacancies(n_vc_query - len(hh.vacancies))
        vacancies.extend(hh.get_formatted_vacancies())
        vacancies.extend(superjob.get_formatted_vacancies())

    json_saver = JSONSaver()
    for vc in vacancies:
        json_saver.add_vacancy(vc)

    json_saver.get_vacancies()

    # Фильтрация
    filter_message = "Желаете отфильтровать вакансии?"
    choices = {
        1: "Да",
        2: "Нет"
    }
    select_filter = select_variant(filter_message, choices)

    if select_filter == 1:
        filter_words = input("Введите ключевые слова для фильтрации вакансий (по имени, опыту или зарплате): ").split()
        vacancies = json_saver.filter_vacancies(filter_words)

        if len(vacancies) == 0:
            print("Нет вакансий, соответствующих заданным критериям.")
            return
        else:
            print("\nОтфильтрованные вакансии:\n")
            for vc in vacancies:
                print(vc)
            print("\n")

    # Сортировка
    sort_message = "Желаете отсортировать вакансии по зарплате?"
    choices = {
        1: "Да",
        2: "Нет"
    }
    print("Сортировка будет производиться по возрастанию.")
    select_sort = select_variant(sort_message, choices)

    if select_sort == 1:
        vacancies = json_saver.sort_vacancies_by_salary()

    print("\nОтсортированные вакансии:\n")
    for vc in vacancies:
        print(vc)


user_interaction()
