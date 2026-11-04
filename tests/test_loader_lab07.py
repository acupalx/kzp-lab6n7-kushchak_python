"""Тести завантаження й перетворення записів на об'єкти (lab07/loader.py)."""

from __future__ import annotations

from pathlib import Path

import pytest

from kzp_lab07.errors import DataError
from kzp_lab07.loader import load_matches, read_rows
from kzp_lab07.models import GroupMatch, PlayoffMatch

HEADER = "home,away,date,home_score,away_score,round,kind\n"


def write_csv(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "matches.csv"
    path.write_text(HEADER + body, encoding="utf-8")
    return path


def test_load_matches_builds_group_match(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "Динамо,Шахтар,2026-03-01,3,0,1,group\n")

    matches = load_matches(path)

    assert len(matches) == 1
    assert isinstance(matches[0], GroupMatch)
    assert matches[0].home == "Динамо"


def test_load_matches_builds_playoff_match(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "Динамо,Шахтар,2026-03-01,2,1,1,playoff\n")

    matches = load_matches(path)

    assert isinstance(matches[0], PlayoffMatch)


def test_load_matches_parses_comma_in_quoted_team_name(tmp_path: Path) -> None:
    path = write_csv(tmp_path, '"Карпати, Львів",Верес,2026-03-02,1,1,1,group\n')

    matches = load_matches(path)

    assert matches[0].home == "Карпати, Львів"


def test_load_matches_on_header_only_file_returns_empty_list(tmp_path: Path) -> None:
    assert load_matches(write_csv(tmp_path, "")) == []


def test_load_matches_on_empty_file_returns_empty_list(tmp_path: Path) -> None:
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")

    assert load_matches(path) == []


def test_read_rows_rejects_missing_required_column(tmp_path: Path) -> None:
    path = tmp_path / "matches.csv"
    path.write_text(
        "home,away,date,home_score,away_score,round\nA,B,2026-01-01,1,0,1\n", encoding="utf-8"
    )

    with pytest.raises(DataError, match="kind"):
        read_rows(path)


def test_load_matches_rejects_unknown_kind(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "Динамо,Шахтар,2026-03-01,3,0,1,final\n")

    with pytest.raises(DataError, match="невідомий тип"):
        load_matches(path)


def test_load_matches_rejects_non_numeric_score(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "Динамо,Шахтар,2026-03-01,два,0,1,group\n")

    with pytest.raises(DataError, match="помилковий формат"):
        load_matches(path)


def test_load_matches_wraps_playoff_draw_as_data_error_with_row_number(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "Динамо,Шахтар,2026-03-01,1,1,1,playoff\n")

    with pytest.raises(DataError, match=r"Рядок 1:.*нічиєю"):
        load_matches(path)


def test_load_matches_rejects_blank_team_name(tmp_path: Path) -> None:
    path = write_csv(tmp_path, " ,Шахтар,2026-03-01,1,0,1,group\n")

    with pytest.raises(DataError, match="порожня назва"):
        load_matches(path)
