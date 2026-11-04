"""Тести завантаження й перевірки записів (loader.py)."""

from __future__ import annotations

from pathlib import Path

import pytest

from kzp_lab06.errors import DataError
from kzp_lab06.loader import load_records, parse_record, read_rows

HEADER = "home,away,date,home_score,away_score,round\n"


def write_csv(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "input.csv"
    path.write_text(HEADER + body, encoding="utf-8")
    return path


def test_load_records_parses_valid_csv(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "Динамо,Шахтар,2026-03-01,3,0,1\n")

    records = load_records(path)

    assert records == [
        {
            "home": "Динамо",
            "away": "Шахтар",
            "date": "2026-03-01",
            "home_score": 3,
            "away_score": 0,
            "round": 1,
        }
    ]


def test_load_records_parses_comma_in_quoted_team_name(tmp_path: Path) -> None:
    path = write_csv(tmp_path, '"Карпати, Львів",Верес,2026-03-02,1,1,1\n')

    records = load_records(path)

    assert records[0]["home"] == "Карпати, Львів"


def test_load_records_on_header_only_file_returns_empty_list(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "")

    assert load_records(path) == []


def test_load_records_on_empty_file_returns_empty_list(tmp_path: Path) -> None:
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")

    assert load_records(path) == []


def test_read_rows_rejects_missing_required_column(tmp_path: Path) -> None:
    path = tmp_path / "input.csv"
    path.write_text("home,away,date,home_score,away_score\nA,B,2026-01-01,1,0\n", encoding="utf-8")

    with pytest.raises(DataError, match="round"):
        read_rows(path)


def test_parse_record_rejects_non_numeric_score() -> None:
    row = {
        "home": "A",
        "away": "B",
        "date": "2026-01-01",
        "home_score": "два",
        "away_score": "0",
        "round": "1",
    }

    with pytest.raises(DataError, match="помилковий формат"):
        parse_record(row, row_number=5)


def test_parse_record_error_includes_row_number() -> None:
    row = {
        "home": "A",
        "away": "B",
        "date": "2026-01-01",
        "home_score": "-1",
        "away_score": "0",
        "round": "1",
    }

    with pytest.raises(DataError, match=r"Рядок 7:.*від'ємним"):
        parse_record(row, row_number=7)


def test_parse_record_rejects_blank_team_name() -> None:
    row = {
        "home": " ",
        "away": "B",
        "date": "2026-01-01",
        "home_score": "1",
        "away_score": "0",
        "round": "1",
    }

    with pytest.raises(DataError, match="порожня назва"):
        parse_record(row, row_number=1)


def test_parse_record_rejects_round_below_one() -> None:
    row = {
        "home": "A",
        "away": "B",
        "date": "2026-01-01",
        "home_score": "1",
        "away_score": "0",
        "round": "0",
    }

    with pytest.raises(DataError, match="тур"):
        parse_record(row, row_number=1)


def test_parse_record_rejects_missing_value_in_row() -> None:
    row = {
        "home": "A",
        "away": "B",
        "date": "2026-01-01",
        "home_score": None,
        "away_score": "0",
        "round": "1",
    }

    with pytest.raises(DataError, match="помилковий формат"):
        parse_record(row, row_number=1)
