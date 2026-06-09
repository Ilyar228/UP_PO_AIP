"""Состояние и обработка нажатий кнопок калькулятора (серверная логика)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from calculator_logic import CalculatorError, calculate, format_result, percent


@dataclass
class CalculatorState:
    current_value: str = "0"
    previous_value: float | None = None
    operator: str | None = None
    waiting_for_operand: bool = False
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "current_value": self.current_value,
            "previous_value": self.previous_value,
            "operator": self.operator,
            "waiting_for_operand": self.waiting_for_operand,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> CalculatorState:
        if not data:
            return cls()
        return cls(
            current_value=data.get("current_value", "0"),
            previous_value=data.get("previous_value"),
            operator=data.get("operator"),
            waiting_for_operand=data.get("waiting_for_operand", False),
            error=data.get("error"),
        )

    def display(self) -> str:
        return self.current_value

    def handle(self, action: str, value: str | None = None) -> None:
        self.error = None

        handlers = {
            "digit": lambda: self._input_digit(value or ""),
            "decimal": self._input_decimal,
            "operator": lambda: self._input_operator(value or ""),
            "equals": self._calculate,
            "clear": self._clear,
            "backspace": self._backspace,
            "percent": self._apply_percent,
        }
        handler = handlers.get(action)
        if handler is None:
            raise ValueError(f"Неизвестное действие: {action}")
        handler()

    def _input_digit(self, digit: str) -> None:
        if self.waiting_for_operand:
            self.current_value = digit
            self.waiting_for_operand = False
        else:
            self.current_value = digit if self.current_value == "0" else self.current_value + digit

    def _input_decimal(self) -> None:
        if self.waiting_for_operand:
            self.current_value = "0."
            self.waiting_for_operand = False
            return
        if "." not in self.current_value:
            self.current_value += "."

    def _input_operator(self, next_operator: str) -> None:
        input_value = float(self.current_value)

        if self.previous_value is not None and self.operator and not self.waiting_for_operand:
            try:
                result = calculate(self.previous_value, self.operator, input_value)
                self.current_value = format_result(result)
                self.previous_value = float(self.current_value)
            except CalculatorError as err:
                self._fail(str(err))
                return
        else:
            self.previous_value = input_value

        self.operator = next_operator
        self.waiting_for_operand = True

    def _calculate(self) -> None:
        if self.operator is None or self.previous_value is None:
            return

        input_value = float(self.current_value)
        try:
            result = calculate(self.previous_value, self.operator, input_value)
            self.current_value = format_result(result)
            self.previous_value = None
            self.operator = None
            self.waiting_for_operand = True
        except CalculatorError as err:
            self._fail(str(err))

    def _clear(self) -> None:
        self.current_value = "0"
        self.previous_value = None
        self.operator = None
        self.waiting_for_operand = False

    def _backspace(self) -> None:
        if self.waiting_for_operand:
            return
        if len(self.current_value) <= 1:
            self.current_value = "0"
        else:
            self.current_value = self.current_value[:-1]

    def _apply_percent(self) -> None:
        value = float(self.current_value)
        self.current_value = format_result(percent(value))

    def _fail(self, message: str) -> None:
        self.error = message
        self._clear()
