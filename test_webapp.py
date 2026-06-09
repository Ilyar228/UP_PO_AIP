"""Интеграционные тесты Flask-приложения WebCalc."""

import sys

from app import app


def _press(client, action: str, value: str | None = None):
    data = {"action": action}
    if value is not None:
        data["value"] = value
    return client.post("/", data=data, follow_redirects=True)


def _display(client) -> str:
    text = client.get("/").data.decode("utf-8")
    start = text.index('<div class="display">') + len('<div class="display">')
    end = text.index("</div>", start)
    return text[start:end].strip()


def _has_error(client, message: str) -> bool:
    return message in client.get("/").data.decode("utf-8")


def main() -> int:
    print("=" * 50)
    print("Интеграционные тесты WebCalc (Flask)")
    print("=" * 50)

    passed = 0
    tests = []

    with app.test_client() as client:
        _press(client, "clear")

        def run(name: str, ok: bool):
            nonlocal passed
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] {name}")
            if ok:
                passed += 1
            tests.append(name)

        _press(client, "digit", "2")
        _press(client, "operator", "+")
        _press(client, "digit", "2")
        _press(client, "equals")
        run("TC-W01: 2 + 2 = 4", _display(client) == "4")

        _press(client, "clear")
        _press(client, "digit", "1")
        _press(client, "digit", "0")
        _press(client, "operator", "-")
        _press(client, "digit", "3")
        _press(client, "equals")
        run("TC-W02: 10 - 3 = 7", _display(client) == "7")

        _press(client, "clear")
        for d in "6":
            _press(client, "digit", d)
        _press(client, "operator", "*")
        _press(client, "digit", "7")
        _press(client, "equals")
        run("TC-W03: 6 * 7 = 42", _display(client) == "42")

        _press(client, "clear")
        _press(client, "digit", "5")
        _press(client, "operator", "/")
        _press(client, "digit", "0")
        _press(client, "equals")
        run("TC-W04: деление на ноль", _has_error(client, "Деление на ноль невозможно"))

        _press(client, "clear")
        run("TC-W05: сброс после ошибки", _display(client) == "0")

    total = len(tests)
    print("-" * 50)
    print(f"Итого: {passed}/{total} тестов пройдено")
    print("=" * 50)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
