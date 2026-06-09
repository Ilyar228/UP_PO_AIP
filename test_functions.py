"""
Unit-тесты для практической работы №3.
Покрывается функция: validate_password (Вариант А).
Запуск: pytest test_functions.py -v
"""

import pytest
from functions import validate_password


# ═══════════════════════════════════════════════════════════
# Тесты для validate_password (Вариант A)
# ═══════════════════════════════════════════════════════════

class TestValidatePassword:
    """Тесты валидации пароля."""

    # --- Позитивные тесты ---

    def test_valid_simple(self):
        """Корректный пароль: 8 символов, есть буква и цифра."""
        assert validate_password("Hello123") is True

    def test_valid_long(self):
        """Длинный корректный пароль — должен проходить."""
        assert validate_password("SecurePassword2024!") is True

    def test_valid_special_chars(self):
        """Специальные символы разрешены, если пароль иначе корректен."""
        assert validate_password("P@ss1word") is True

    def test_valid_exactly_8_chars(self):
        """Граничный случай: ровно 8 символов — минимально допустимо."""
        assert validate_password("Ab1cdefg") is True

    # --- Негативные тесты ---

    def test_too_short(self):
        """Пароль из 7 символов — слишком короткий."""
        assert validate_password("Ab1cde7") is False

    def test_no_digits(self):
        """Только буквы — нет ни одной цифры."""
        assert validate_password("Abcdefgh") is False

    def test_no_letters(self):
        """Только цифры — нет ни одной буквы."""
        assert validate_password("12345678") is False

    def test_has_space(self):
        """Пароль с пробелом — недопустим."""
        assert validate_password("Hello 123") is False

    # --- Граничные случаи ---

    def test_exactly_7_chars(self):
        """7 символов — на единицу меньше минимума."""
        assert validate_password("Ab1cde7") is False

    def test_empty_string(self):
        """Пустая строка — слишком короткая и без символов."""
        assert validate_password("") is False

    def test_only_spaces(self):
        """Строка только из пробелов."""
        assert validate_password("        ") is False

    # --- Ошибочные данные ---

    def test_invalid_type_none(self):
        """None вместо строки — должен бросать TypeError."""
        with pytest.raises(TypeError):
            validate_password(None)

    def test_invalid_type_int(self):
        """Целое число вместо строки — должен бросать TypeError."""
        with pytest.raises(TypeError):
            validate_password(12345678)

    # --- Параметризованный тест ---

    @pytest.mark.parametrize("pwd, expected", [
        ("Short1",       False),   # слишком короткий
        ("NoDigits!",    False),   # нет цифры
        ("12345678",     False),   # нет буквы
        ("Has Space1",   False),   # пробел
        ("Valid1Pass",   True),    # корректный
        ("AnotherOk2",  True),    # корректный
    ])
    def test_parametrized_passwords(self, pwd, expected):
        """Параметризованная проверка набора паролей."""
        assert validate_password(pwd) == expected
