"""Читає CSV-файл варіанта 17 («Спортивна ліга») і перетворює рядки на об'єкти `Match`.

Формат одного запису: ``home,away,date,home_score,away_score,round,kind``, де
``kind`` — ``group`` або ``playoff`` і визначає, який підтип створити.
Валідація відбувається під час створення об'єкта — `analysis.py` отримує
лише коректні матчі.
"""

from __future__ import annotations

import csv
from pathlib import Path

from kzp_lab07.errors import DataError
from kzp_lab07.models import GroupMatch, Match, PlayoffMatch

REQUIRED_FIELDS = ("home", "away", "date", "home_score", "away_score", "round", "kind")

_BUILDERS = {"group": GroupMatch, "playoff": PlayoffMatch}


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


def build_match(row: dict[str, str], row_number: int) -> Match:
    """Перевіряє й перетворює один рядок CSV на об'єкт відповідного підтипу `Match`.

    :raises DataError: з номером рядка й причиною, якщо дані некоректні.
    """
    home = (row.get("home") or "").strip()
    away = (row.get("away") or "").strip()
    date = (row.get("date") or "").strip()

    try:
        home_score = int(row["home_score"])
        away_score = int(row["away_score"])
        round_number = int(row["round"])
    except (KeyError, TypeError, ValueError) as error:
        raise DataError(f"Рядок {row_number}: числове поле має помилковий формат") from error

    kind = (row.get("kind") or "").strip().lower()
    builder = _BUILDERS.get(kind)
    if builder is None:
        raise DataError(f"Рядок {row_number}: невідомий тип матчу '{kind}'")

    try:
        return builder(home, away, date, home_score, away_score, round_number)
    except ValueError as error:
        raise DataError(f"Рядок {row_number}: {error}") from error


def load_matches(path: Path) -> list[Match]:
    """Читає й перетворює всі записи CSV-файла.

    Порожній файл (лише заголовок або зовсім порожній) дає порожній список,
    а не помилку — це різні, але обидва допустимі випадки.
    """
    return [build_match(row, row_number) for row_number, row in enumerate(read_rows(path), start=1)]
