"""Тести обчислень над записами матчів (analysis.py)."""

from __future__ import annotations

import pytest

from kzp_lab06.analysis import build_summary, count_by_round, matches_in_round, unique_teams

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


def test_matches_in_round_filters_exact_round() -> None:
    selected = matches_in_round(RECORDS, 2)

    assert len(selected) == 2
    assert all(record["round"] == 2 for record in selected)


def test_matches_in_round_returns_empty_list_when_round_absent() -> None:
    assert matches_in_round(RECORDS, 99) == []


def test_count_by_round_groups_and_sorts_keys() -> None:
    assert count_by_round(RECORDS) == {1: 2, 2: 2, 3: 1, 4: 2, 5: 1}


def test_count_by_round_on_empty_input_returns_empty_dict() -> None:
    assert count_by_round([]) == {}


def test_unique_teams_deduplicates_repeated_names() -> None:
    teams = unique_teams(RECORDS)

    assert teams == {
        "Динамо",
        "Шахтар",
        "Карпати, Львів",
        "Верес",
        "Зоря",
        "Металіст",
        "Оболонь",
        "Полісся",
        "Рух",
        "Колос",
    }
    assert len(teams) == 10


def test_build_summary_computes_total_goals_and_max_difference() -> None:
    summary = build_summary(RECORDS, "total_goals", "max_difference", min_round=1)

    assert summary["count"] == 8
    assert summary["total_goals"] == 26.0
    assert summary["max_difference"] == 3.0


def test_build_summary_filters_by_min_round() -> None:
    summary = build_summary(
        RECORDS,
        "total_goals",
        "max_difference",
        min_round=3,
        total_goals="Голів",
        max_difference="Різниця",
    )

    assert summary["count"] == 4
    assert summary["Голів"] == 12.0
    assert summary["Різниця"] == 3.0


def test_build_summary_empty_selection_returns_zero_valued_metrics() -> None:
    summary = build_summary(RECORDS, "total_goals", "max_difference", min_round=99)

    assert summary["count"] == 0
    assert summary["total_goals"] == 0.0
    assert summary["max_difference"] == 0.0


def test_build_summary_rejects_unknown_metric() -> None:
    with pytest.raises(ValueError, match="Невідома метрика"):
        build_summary(RECORDS, "goals_per_minute")


def test_build_summary_default_min_round_is_one() -> None:
    assert build_summary(RECORDS, "total_goals")["count"] == len(RECORDS)
