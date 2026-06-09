# calculator.py — тестируемый модуль

def add(a, b):
    """Сложение двух чисел"""
    return a + b

def divide(a, b):
    """Деление a на b"""
    if b == 0:
        raise ValueError("Деление на ноль недопустимо")
    return a / b

def power(base, exp):
    """Возведение base в степень exp"""
    return base ** exp
