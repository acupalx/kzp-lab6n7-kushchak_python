"""Тести інтерфейсу командного рядка лаб. 7 (cli.py)."""

from __future__ import annotations

from pathlib import Path

from kzp_lab07.cli import main

VALID_CSV = (
    "home,away,date,home_score,away_score,round,kind\n"
    "Динамо,Шахтар,2026-03-01,2,1,1,group\n"
    "Шахтар,Динамо,2026-03-08,1,0,2,playoff\n"
)

BROKEN_CSV = (
    "home,away,date,home_score,away_score,round,kind\nДинамо,Шахтар,2026-03-01,1,1,1,playoff\n"
)


def test_cli_success_returns_zero_and_writes_report(tmp_path: Path, capsys) -> None:
    input_path = tmp_path / "matches.csv"
    output_path = tmp_path / "reports" / "summary.txt"
    input_path.write_text(VALID_CSV, encoding="utf-8")

    exit_code = main([str(input_path), str(output_path)])

    assert exit_code == 0
    assert "Турнірна таблиця" in output_path.read_text(encoding="utf-8")
    assert "Звіт записано" in capsys.readouterr().out


def test_cli_reports_data_error_with_exit_code_one(tmp_path: Path, capsys) -> None:
    input_path = tmp_path / "matches.csv"
    output_path = tmp_path / "reports" / "summary.txt"
    input_path.write_text(BROKEN_CSV, encoding="utf-8")

    exit_code = main([str(input_path), str(output_path)])

    assert exit_code == 1
    assert not output_path.exists()
    assert "Помилка даних" in capsys.readouterr().err


def test_cli_missing_input_file_returns_exit_code_one(tmp_path: Path, capsys) -> None:
    exit_code = main([str(tmp_path / "немає.csv"), str(tmp_path / "summary.txt")])

    assert exit_code == 1
    assert "Помилка файлової системи" in capsys.readouterr().err


def test_cli_wrong_argument_count_returns_exit_code_two(capsys) -> None:
    exit_code = main(["тільки-один-аргумент"])

    assert exit_code == 2
    assert "Використання" in capsys.readouterr().err
