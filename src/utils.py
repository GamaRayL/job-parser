from src.vacancy_api import HeadHunterAPI, SuperJobAPI
from src.vacancy_manager import JSONSaver


def select_variant(message, variants):
    """

    :return:
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


# def choose_filter():
#     is_filter = input("Отфильтровать вакансии: \n"
#                       "1. Да\n"
#                       "2. Нет\n")
#
#     while True:
#         try:
#             is_filter in [1, 2]
#         except ValueError:
#             print("Выберите вариант из ")
#             continue

def user_interaction():
    """

    :return:
    """
    print("Добро пожаловать в программу для поиска вакансий!\n")
    platform_message = "Выберите пожалуйста платформу для поиска (указав цифру):"
    platforms = {
        1: "HeadHunter",
        2: "SuperJob",
        3: "На всех",
        4: "Завершить программу"
    }
    select_platform = select_variant(platform_message, platforms)

    if select_platform == 4:
        exit()

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
        for api in (hh, superjob):
            n_half_vc = int(n_vc_query / 2)
            api.get_vacancies(n_half_vc)
            vacancies.extend(api.get_formatted_vacancies())

    json_saver = JSONSaver()
    for vc in vacancies:
        json_saver.add_vacancy(vc)

    json_saver.get_vacancies()

    # Фильтрация
    filter_message = "Отфильтровать вакансии?"
    choices = {
        1: "Да",
        2: "Нет"
    }
    select_filter = select_variant(filter_message, choices)

    if select_filter == 1:
        filter_words = input("Введите ключевые слова для фильтрации вакансий (по имени, опыту или зп): ").split()
        vacancies = json_saver.filter_vacancies(filter_words)

        if not vacancies:
            print("Нет вакансий, соответствующих заданным критериям.")
            return

    else:
        vacancies = json_saver.get_vacancies()

    # Сортировка
    sort_message = "Отсортировать вакансию по зарплате?"
    choices = {
        1: "Да",
        2: "Нет"
    }
    select_sort = select_variant(sort_message, choices)

    if select_sort == 1:
        vacancies = json_saver.sort_vacancies_by_salary()
    else:
        return vacancies

    for vc in vacancies:
        print(vc)


user_interaction()

# search_query = input("Введите поисковый запрос: ")
# top_n = int(input("Введите количество вакансий для вывода в топ N: "))
# filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
# filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)
#
# if not filtered_vacancies:
#     print("Нет вакансий, соответствующих заданным критериям.")
#     return
#
# sorted_vacancies = sort_vacancies(filtered_vacancies)
# top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
# print_vacancies(top_vacancies)


# Создать функцию для взаимодействия с пользователем. Функция должна взаимодействовать с пользователем через консоль.
# Самостоятельно придумать сценарии и возможности взаимодействия с пользователем.
# Например, позволять пользователю указать, с каких платформ он хочет получить вакансии,
# ввести поисковый запрос, получить топ N вакансий по зарплате, получить вакансии в отсортированном виде,
# получить вакансии, в описании которых есть определенные ключевые слова, например "postgres" и т. п.
