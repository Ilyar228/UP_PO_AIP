"""Арифметическая логика калькулятора WebCalc."""


class CalculatorError(Exception):
    pass


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise CalculatorError("Деление на ноль невозможно")
    return a / b


def percent(value: float) -> float:
    return value / 100


def calculate(a: float, operator: str, b: float) -> float:
    ops = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    if operator not in ops:
        raise CalculatorError("Неизвестная операция")
    return ops[operator](a, b)


def format_result(value: float) -> str:
    if not isinstance(value, (int, float)) or value != value:  # NaN check
        raise CalculatorError("Результат не является числом")
    rounded = round(value * 1e10) / 1e10
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)
