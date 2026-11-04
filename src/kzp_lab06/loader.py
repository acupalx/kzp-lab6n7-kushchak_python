"""Читає CSV-файл варіанта 17 («Спортивна ліга») і перетворює рядки на типізовані записи.

Формат одного запису: ``home,away,date,home_score,away_score,round``. Вхідний
файл не змінюється — дані лише читаються в пам'ять.
"""

from __future__ import annotations

import csv
from pathlib import Path

from kzp_lab06.errors import DataError

REQUIRED_FIELDS = ("home", "away", "date", "home_score", "away_score", "round")


def read_rows(path: Path) -> list[dict[str, str]]:
    """Читає CSV-файл і повертає його рядки як словники рядкових значень.

    :raises DataError: якщо в заголовку файла бракує обов'язкових полів.
    """
    # newline="" передає керування роздільниками рядків модулю csv.
    with path.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is not None:
            missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
            if missing:
                raise DataError(f"У заголовку CSV бракує полів: {', '.join(missing)}")
        return list(reader)


def parse_record(row: dict[str, str], row_number: int) -> dict[str, object]:
    """Перевіряє й перетворює один рядок CSV на типізований запис матчу.

    Перетворює ``home_score``, ``away_score`` і ``round`` на ``int``; перевіряє
    непорожні назви команд і дату, невід'ємний рахунок та тур не менше 1.

    :raises DataError: з номером рядка й причиною, якщо дані некоректні.
    """
    home = (row.get("home") or "").strip()
    away = (row.get("away") or "").strip()
    date = (row.get("date") or "").strip()
    if not home or not away:
        raise DataError(f"Рядок {row_number}: порожня назва команди")
    if not date:
        raise DataError(f"Рядок {row_number}: порожня дата")

    try:
        home_score = int(row["home_score"])
        away_score = int(row["away_score"])
        round_number = int(row["round"])
    except (KeyError, TypeError, ValueError) as error:
        raise DataError(f"Рядок {row_number}: числове поле має помилковий формат") from error

    if home_score < 0 or away_score < 0:
        raise DataError(f"Рядок {row_number}: рахунок не може бути від'ємним")
    if round_number < 1:
        raise DataError(f"Рядок {row_number}: тур має бути не менше 1")

    return {
        "home": home,
        "away": away,
        "date": date,
        "home_score": home_score,
        "away_score": away_score,
        "round": round_number,
    }


def load_records(path: Path) -> list[dict[str, object]]:
    """Читає й перетворює всі записи CSV-файла.

    Порожній файл (лише заголовок або зовсім порожній) дає порожній список,
    а не помилку — це різні, але обидва допустимі випадки.
    """
    return [
        parse_record(row, row_number) for row_number, row in enumerate(read_rows(path), start=1)
    ]
