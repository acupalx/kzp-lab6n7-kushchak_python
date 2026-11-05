"""Тести обчислень над об'єктами Match (lab07/analysis.py)."""

from __future__ import annotations

from kzp_lab07.analysis import (
    build_standings,
    count_by_round,
    matches_in_round,
    max_score_difference,
    total_goals,
    unique_teams,
)
from kzp_lab07.models import GroupMatch, PlayoffMatch

MATCHES = [
    GroupMatch("Динамо", "Шахтар", "2026-03-01", 3, 0, 1),
    GroupMatch("Карпати", "Верес", "2026-03-02", 1, 1, 1),
    GroupMatch("Зоря", "Металіст", "2026-03-08", 2, 2, 2),
]


def test_matches_in_round_filters_exact_round() -> None:
    assert len(matches_in_round(MATCHES, 1)) == 2


def test_matches_in_round_returns_empty_list_when_round_absent() -> None:
    assert matches_in_round(MATCHES, 99) == []


def test_count_by_round_groups_and_sorts_keys() -> None:
    assert count_by_round(MATCHES) == {1: 2, 2: 1}


def test_unique_teams_deduplicates_repeated_names() -> None:
    matches = [*MATCHES, GroupMatch("Динамо", "Зоря", "2026-03-09", 1, 0, 2)]

    assert unique_teams(matches) == {"Динамо", "Шахтар", "Карпати", "Верес", "Зоря", "Металіст"}


def test_total_goals_sums_all_matches() -> None:
    assert total_goals(MATCHES) == 9.0


def test_max_score_difference_finds_largest_margin() -> None:
    assert max_score_difference(MATCHES) == 3.0


def test_max_score_difference_on_empty_input_is_zero() -> None:
    assert max_score_difference([]) == 0.0


def test_build_standings_works_polymorphically_across_subtypes() -> None:
    # Жодного isinstance за конкретним підтипом -- лише виклик через points().
    mixed = [
        GroupMatch("A", "B", "2026-04-01", 2, 1, 1),
        PlayoffMatch("B", "A", "2026-04-08", 2, 0, 2),
    ]

    standings = build_standings(mixed)

    assert standings[0].team == "A"
    assert standings[0].points == 3
    assert standings[0].played == 2
    assert standings[0].goal_difference == -1

    assert standings[1].team == "B"
    assert standings[1].points == 2
    assert standings[1].goal_difference == 1


def test_build_standings_on_empty_input_returns_empty_list() -> None:
    assert build_standings([]) == []
