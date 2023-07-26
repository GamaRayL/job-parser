from typing import Dict


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
