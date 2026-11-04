"""Тести формування й запису текстового звіту (reporting.py)."""

from __future__ import annotations

from pathlib import Path

from kzp_lab06.reporting import format_report, write_report

RECORDS = [
    {
        "home": "Динамо",
        "away": "Шахтар",
        "date": "2026-03-01",
        "home_score": 3,
        "away_score": 0,
        "round": 1,
    },
    {
        "home": "Карпати, Львів",
        "away": "Верес",
        "date": "2026-03-02",
        "home_score": 1,
        "away_score": 1,
        "round": 1,
    },
    {
        "home": "Зоря",
        "away": "Металіст",
        "date": "2026-03-08",
        "home_score": 2,
        "away_score": 2,
        "round": 2,
    },
    {
        "home": "Оболонь",
        "away": "Полісся",
        "date": "2026-03-09",
        "home_score": 4,
        "away_score": 1,
        "round": 2,
    },
    {
        "home": "Рух",
        "away": "Колос",
        "date": "2026-03-15",
        "home_score": 0,
        "away_score": 3,
        "round": 3,
    },
    {
        "home": "Динамо",
        "away": "Шахтар",
        "date": "2026-03-22",
        "home_score": 1,
        "away_score": 1,
        "round": 4,
    },
    {
        "home": "Верес",
        "away": "Карпати, Львів",
        "date": "2026-03-23",
        "home_score": 0,
        "away_score": 0,
        "round": 4,
    },
    {
        "home": "Шахтар",
        "away": "Зоря",
        "date": "2026-03-30",
        "home_score": 5,
        "away_score": 2,
        "round": 5,
    },
]

EXPECTED_REPORT = (
    "Записів: 8\n"
    "Унікальних команд: 10\n"
    "Тур 1: 2 матчів\n"
    "Тур 2: 2 матчів\n"
    "Тур 3: 1 матчів\n"
    "Тур 4: 2 матчів\n"
    "Тур 5: 1 матчів\n"
    "Матчів від туру 3: 4\n"
    "Голів від туру 3: 12.00\n"
    "Макс. різниця від туру 3: 3.00\n"
)


def test_format_report_is_deterministic_and_matches_expected_text() -> None:
    assert format_report(RECORDS) == EXPECTED_REPORT


def test_format_report_twice_gives_identical_text() -> None:
    assert format_report(RECORDS) == format_report(RECORDS)


def test_format_report_on_empty_records() -> None:
    report = format_report([])

    assert "Записів: 0" in report
    assert "Унікальних команд: 0" in report
    assert "Матчів від туру 3: 0" in report


def test_write_report_writes_utf8_file_with_unix_newline(tmp_path: Path) -> None:
    output = tmp_path / "reports" / "summary.txt"

    write_report(output, "Готово\n")

    assert output.read_text(encoding="utf-8") == "Готово\n"


def test_write_report_creates_missing_parent_directory(tmp_path: Path) -> None:
    output = tmp_path / "nested" / "dir" / "summary.txt"

    write_report(output, "ок\n")

    assert output.exists()
