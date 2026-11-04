"""Інтерфейс командного рядка: читає CSV, формує звіт і записує його у файл.

Код запуску виконується лише через ``if __name__ == "__main__":`` — імпорт
модуля не друкує нічого й не чіпає файлову систему.
"""

from __future__ import annotations

import sys
from pathlib import Path

from kzp_lab07.errors import DataError
from kzp_lab07.loader import load_matches
from kzp_lab07.reporting import format_report, write_report


def run(input_path: Path, output_path: Path) -> None:
    """Виконує повний конвеєр: завантаження CSV, аналіз і запис звіту."""
    matches = load_matches(input_path)
    write_report(output_path, format_report(matches))


def main(argv: list[str] | None = None) -> int:
    """Точка входу CLI.

    :return: ``0`` після успіху, ``1`` для помилки даних чи файлової системи,
        ``2`` для неправильної кількості аргументів.
    """
    # Явний UTF-8 для stdout/stderr: консоль Windows інколи має інше кодування.
    # hasattr-перевірка потрібна, бо під pytest stdout/stderr підмінені
    # об'єктами захоплення виводу без методу reconfigure.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 2:
        print("Використання: kzp-lab07 <вхідний.csv> <звіт.txt>", file=sys.stderr)
        return 2

    input_path, output_path = Path(args[0]), Path(args[1])
    try:
        run(input_path, output_path)
    except DataError as error:
        # Очікувана помилка даних -- зрозуміле повідомлення, не traceback.
        print(f"Помилка даних: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Помилка файлової системи: {error}", file=sys.stderr)
        return 1

    print(f"Звіт записано: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
