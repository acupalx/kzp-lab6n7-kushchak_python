"""Тести моделі матчу (models.py): @property, спеціальні методи й підтипи."""

from __future__ import annotations

import pytest

from kzp_lab07.models import GroupMatch, PlayoffMatch


def test_constructor_stores_valid_fields() -> None:
    match = GroupMatch("Динамо", "Шахтар", "2026-03-01", 3, 0, 1)

    assert match.home == "Динамо"
    assert match.away == "Шахтар"
    assert match.round == 1
    assert match.kind == "група"


def test_constructor_rejects_blank_home_team() -> None:
    with pytest.raises(ValueError, match="порожня назва"):
        GroupMatch(" ", "Шахтар", "2026-03-01", 3, 0, 1)


def test_constructor_rejects_negative_score() -> None:
    with pytest.raises(ValueError, match="від'ємним"):
        GroupMatch("Динамо", "Шахтар", "2026-03-01", -1, 0, 1)


def test_round_setter_accepts_boundary_value_one() -> None:
    match = GroupMatch("Динамо", "Шахтар", "2026-03-01", 3, 0, 1)

    assert match.round == 1


def test_round_setter_rejects_value_below_one() -> None:
    with pytest.raises(ValueError, match="тур"):
        GroupMatch("Динамо", "Шахтар", "2026-03-01", 3, 0, 0)


def test_round_setter_rejects_reassignment_below_one() -> None:
    match = GroupMatch("Динамо", "Шахтар", "2026-03-01", 3, 0, 2)

    with pytest.raises(ValueError, match="тур"):
        match.round = 0


def test_str_contains_teams_score_and_kind() -> None:
    match = GroupMatch("Динамо", "Шахтар", "2026-03-01", 3, 0, 1)

    text = str(match)

    assert "Динамо" in text
    assert "3:0" in text
    assert "група" in text


def test_repr_contains_concrete_subtype_name() -> None:
    match = PlayoffMatch("Динамо", "Шахтар", "2026-03-01", 2, 1, 1)

    assert repr(match).startswith("PlayoffMatch(")


def test_equal_matches_of_same_subtype_compare_equal() -> None:
    # "Дубльоване значення" варіанта: два незалежно створені об'єкти з
    # однаковими полями мають бути рівними.
    first = GroupMatch("Динамо", "Шахтар", "2026-03-01", 3, 0, 1)
    second = GroupMatch("Динамо", "Шахтар", "2026-03-01", 3, 0, 1)

    assert first == second


def test_matches_of_different_subtypes_with_same_fields_are_not_equal() -> None:
    group = GroupMatch("Динамо", "Шахтар", "2026-03-01", 2, 1, 1)
    playoff = PlayoffMatch("Динамо", "Шахтар", "2026-03-01", 2, 1, 1)

    assert group != playoff


def test_eq_returns_not_implemented_for_incompatible_type() -> None:
    match = GroupMatch("Динамо", "Шахтар", "2026-03-01", 3, 0, 1)

    assert match.__eq__(42) is NotImplemented


def test_group_match_winner_gets_three_points() -> None:
    match = GroupMatch("Динамо", "Шахтар", "2026-03-01", 2, 1, 1)

    assert match.points() == (3, 0)


def test_group_match_draw_gives_one_point_each() -> None:
    match = GroupMatch("Карпати", "Верес", "2026-03-01", 1, 1, 1)

    assert match.points() == (1, 1)


def test_playoff_match_winner_gets_two_points() -> None:
    match = PlayoffMatch("Динамо", "Шахтар", "2026-03-01", 2, 1, 1)

    assert match.points() == (2, 0)
    assert PlayoffMatch("Динамо", "Шахтар", "2026-03-01", 0, 1, 1).points() == (0, 2)


def test_playoff_match_rejects_draw() -> None:
    with pytest.raises(ValueError, match="нічиєю"):
        PlayoffMatch("Динамо", "Шахтар", "2026-03-01", 1, 1, 1)
