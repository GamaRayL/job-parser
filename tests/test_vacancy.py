# import copy
#
# import pytest
#
# from src.vacancy import Vacancy
#
#
# @pytest.fixture
# def vacancy():
#     return Vacancy('SkyPro', 'https://hh.ru/vacancy/123456', 'Python Developer', 120000, 160000,
#                    'Требования: опыт работы от 3 лет...',
#                    'Минимальные требования к знаниям и навыкам для отклика:...')
#
#
# def test_vacancy_compare(vacancy):
#     vacancy2 = copy.copy(vacancy)
#     vacancy3 = copy.copy(vacancy)
#     vacancy4 = copy.copy(vacancy)
#
#     vacancy2.salary_from = 130000
#     vacancy2.salary_to = 150000
#
#     vacancy3.salary_from = 120000
#     vacancy3.salary_to = 0
#
#     vacancy4.salary_from = 0
#     vacancy4.salary_to = 120000
#
#     assert vacancy3 == vacancy4
#     assert vacancy2 < vacancy
#     assert vacancy > vacancy4
#
#
# def test_validate_salary(vacancy):
#     with pytest.raises(ValueError, match='Зарплата должна быть числом'):
#         vacancy.salary_to = 'brrr'
#     with pytest.raises(ValueError, match='Зарплата не может быть отрицательной'):
#         vacancy.salary_to = -2
#     with pytest.raises(ValueError, match='Зарплата должна быть числом'):
#         vacancy.salary_from = 'brr'
#     with pytest.raises(ValueError, match='Зарплата не может быть отрицательной'):
#         vacancy.salary_from = -1
#
#     assert vacancy.salary_from == 120000
#     assert vacancy.salary_to == 160000
#
