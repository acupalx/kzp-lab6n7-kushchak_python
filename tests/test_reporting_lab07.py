"""Тести формування текстового звіту з турнірною таблицею (lab07/reporting.py)."""

from __future__ import annotations

from kzp_lab07.models import GroupMatch, PlayoffMatch
from kzp_lab07.reporting import format_report

MATCHES = [
    GroupMatch("Динамо", "Шахтар", "2026-03-01", 2, 1, 1),
    PlayoffMatch("Шахтар", "Динамо", "2026-03-08", 1, 0, 2),
]

EXPECTED_REPORT = (
    "Записів: 2\n"
    "Унікальних команд: 2\n"
    "Тур 1: 1 матчів\n"
    "Тур 2: 1 матчів\n"
    "Загальна кількість голів: 4.00\n"
    "Найбільша різниця рахунку: 1.00\n"
    "Турнірна таблиця:\n"
    "1. Динамо: 3 очок, 2 матчів, різниця +0\n"
    "2. Шахтар: 2 очок, 2 матчів, різниця +0\n"
)


def test_format_report_is_deterministic_and_matches_expected_text() -> None:
    assert format_report(MATCHES) == EXPECTED_REPORT


def test_format_report_twice_gives_identical_text() -> None:
    assert format_report(MATCHES) == format_report(MATCHES)


def test_format_report_on_empty_input() -> None:
    report = format_report([])

    assert "Записів: 0" in report
    assert "Турнірна таблиця:" in report
