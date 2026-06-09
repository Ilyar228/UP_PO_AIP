"""
Модуль с функциями для unit-тестирования.
Практическая работа №3 — Unit-тестирование в Python.
"""

# ─────────────────────────────────────────────
# Вариант A: Валидация пароля
# ─────────────────────────────────────────────

def validate_password(password: str) -> bool:
    """
    Проверяет корректность пароля по следующим критериям:
    - минимум 8 символов
    - минимум 1 цифра
    - минимум 1 буква (латинская или кириллица)
    - не допускаются пробелы

    :param password: строка для проверки
    :return: True — пароль корректен, False — не корректен
    :raises TypeError: если аргумент не является строкой
    """
    if not isinstance(password, str):
        raise TypeError(f"Ожидается строка, получено: {type(password).__name__}")

    if len(password) < 8:
        return False
    if " " in password:
        return False
    if not any(ch.isdigit() for ch in password):
        return False
    if not any(ch.isalpha() for ch in password):
        return False
    return True
