"""
НАМЕРЕННО СЛОМАННАЯ версия функций — для демонстрации ценности тестов.
Ошибки внесены в каждую функцию.
"""

# Вариант A: Валидация пароля — ОШИБКА: порог длины изменён с 8 на 10
def validate_password(password: str) -> bool:
    if not isinstance(password, str):
        raise TypeError(f"Ожидается строка, получено: {type(password).__name__}")
    if len(password) < 10:          # БАГ: было 8, стало 10
        return False
    if " " in password:
        return False
    if not any(ch.isdigit() for ch in password):
        return False
    if not any(ch.isalpha() for ch in password):
        return False
    return True
