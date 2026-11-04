"""Пакет лабораторної роботи № 7 — об'єктно-орієнтована обробка варіанта 17 («Спортивна ліга»)."""

from kzp_lab07.analysis import build_standings, count_by_round, matches_in_round, unique_teams
from kzp_lab07.errors import DataError
from kzp_lab07.loader import load_matches
from kzp_lab07.models import GroupMatch, Match, PlayoffMatch, PointsEarning, TeamStanding
from kzp_lab07.reporting import format_report, write_report

__all__ = [
    "DataError",
    "GroupMatch",
    "Match",
    "PlayoffMatch",
    "PointsEarning",
    "TeamStanding",
    "build_standings",
    "count_by_round",
    "format_report",
    "load_matches",
    "matches_in_round",
    "unique_teams",
    "write_report",
]
