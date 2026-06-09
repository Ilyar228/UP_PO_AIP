"""
Автоматизированные тесты логики веб-калькулятора WebCalc.
Запуск: python test_calculator.py
"""

import sys
from calculator_logic import (
    add,
    subtract,
    multiply,
    divide,
    percent,
    calculate,
    format_result,
    CalculatorError,
)


def run_test(name: str, condition: bool, details: str = "") -> bool:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}" + (f" — {details}" if details and not condition else ""))
    return condition


def main() -> int:
    print("=" * 50)
    print("Автотесты WebCalc — логика калькулятора")
    print("=" * 50)

    passed = 0
    total = 0

    tests = [
        ("TC-A01: Сложение 2 + 2", lambda: add(2, 2) == 4),
        ("TC-A02: Вычитание 10 - 3", lambda: subtract(10, 3) == 7),
        ("TC-A03: Умножение 6 * 7", lambda: multiply(6, 7) == 42),
        ("TC-A04: Деление 15 / 3", lambda: divide(15, 3) == 5),
        ("TC-A05: Деление на ноль", lambda: _test_divide_by_zero()),
        ("TC-A06: Процент 50%", lambda: percent(50) == 0.5),
        ("TC-A07: Дробные числа 0.1 + 0.2", lambda: abs(add(0.1, 0.2) - 0.3) < 1e-9),
        ("TC-A08: Цепочка через calculate", lambda: calculate(100, "-", 37) == 63),
        ("TC-A09: Форматирование результата", lambda: format_result(42.0) == "42"),
        ("TC-A10: Неизвестная операция", lambda: _test_unknown_op()),
    ]

    for name, test_fn in tests:
        total += 1
        try:
            result = test_fn()
            if run_test(name, result):
                passed += 1
        except Exception as e:
            run_test(name, False, str(e))

    print("-" * 50)
    print(f"Итого: {passed}/{total} тестов пройдено")
    print("=" * 50)
    return 0 if passed == total else 1


def _test_divide_by_zero() -> bool:
    try:
        divide(10, 0)
        return False
    except CalculatorError as e:
        return "ноль" in str(e).lower()


def _test_unknown_op() -> bool:
    try:
        calculate(1, "%", 2)
        return False
    except CalculatorError:
        return True


if __name__ == "__main__":
    sys.exit(main())
