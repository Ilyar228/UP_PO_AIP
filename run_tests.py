"""Запуск всех автотестов и сохранение вывода для отчёта."""

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "screenshots" / "autotest_output.txt"


def main() -> int:
    scripts = ["test_calculator.py", "test_webapp.py"]
    lines: list[str] = []

    for script in scripts:
        lines.append(f"=== {script} ===")
        result = subprocess.run(
            [sys.executable, str(BASE / script)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        lines.append(result.stdout)
        if result.stderr:
            lines.append(result.stderr)

    OUTPUT.parent.mkdir(exist_ok=True)
    text = "\n".join(lines)
    OUTPUT.write_text(text, encoding="utf-8")
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("utf-8", errors="replace").decode("cp1251", errors="replace"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
