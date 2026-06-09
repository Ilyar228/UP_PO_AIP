# test_calculator.py — автоматические тесты (pytest)
import pytest
from calculator import add, divide, power


# ===== Тесты функции add =====

def test_add_positive():
    assert add(5, 3) == 8

def test_add_negative():
    assert add(10, -3) == 7

def test_add_zeros():
    assert add(0, 0) == 0

def test_add_large_numbers():
    assert add(10**18, 1) == 10**18 + 1

def test_add_string_raises():
    with pytest.raises(TypeError):
        add(5, "abc")


# ===== Тесты функции divide =====

def test_divide_positive():
    assert divide(10, 2) == 5.0

def test_divide_by_one():
    assert divide(7, 1) == 7.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Деление на ноль"):
        divide(5, 0)

def test_divide_zero_by_number():
    assert divide(0, 5) == 0.0

def test_divide_negative():
    assert divide(-9, 3) == -3.0


# ===== Тесты функции power =====

def test_power_positive():
    assert power(4, 2) == 16

def test_power_zero_exp():
    assert power(100, 0) == 1

def test_power_zero_base_zero_exp():
    assert power(0, 0) == 1

def test_power_negative_exp():
    assert power(2, -1) == 0.5

def test_power_string_raises():
    with pytest.raises(TypeError):
        power("abc", 2)
