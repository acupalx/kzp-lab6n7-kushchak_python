"""Пакет лабораторної роботи № 6 — обробка CSV варіанта 17 («Спортивна ліга») засобами Python."""

from kzp_lab06.analysis import build_summary, count_by_round, matches_in_round, unique_teams
from kzp_lab06.errors import DataError
from kzp_lab06.loader import load_records
from kzp_lab06.reporting import format_report, write_report

__all__ = [
    "DataError",
    "build_summary",
    "count_by_round",
    "format_report",
    "load_records",
    "matches_in_round",
    "unique_teams",
    "write_report",
]
