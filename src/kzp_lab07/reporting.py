"""Формує детермінований текстовий звіт над об'єктами `Match`.

Зберігає показники лаб. 6 (кількість записів, унікальні команди, матчі за
туром, сумарні голи, найбільша різниця рахунку) і додає нову турнірну
таблицю. Не читає CSV і не знає про аргументи командного рядка.
"""

from __future__ import annotations

from pathlib import Path

from kzp_lab07.analysis import (
    build_standings,
    count_by_round,
    max_score_difference,
    total_goals,
    unique_teams,
)
from kzp_lab07.models import Match


def format_report(matches: list[Match]) -> str:
    """Форматує підсумок у детермінований текстовий звіт."""
    rounds = count_by_round(matches)
    teams = unique_teams(matches)
    standings = build_standings(matches)

    lines = [
        f"Записів: {len(matches)}",
        f"Унікальних команд: {len(teams)}",
    ]
    for round_number in sorted(rounds):
        lines.append(f"Тур {round_number}: {rounds[round_number]} матчів")
    lines.append(f"Загальна кількість голів: {total_goals(matches):.2f}")
    lines.append(f"Найбільша різниця рахунку: {max_score_difference(matches):.2f}")
    lines.append("Турнірна таблиця:")
    for position, row in enumerate(standings, start=1):
        summary = f"{row.points} очок, {row.played} матчів, різниця {row.goal_difference:+d}"
        lines.append(f"{position}. {row.team}: {summary}")
    return "\n".join(lines) + "\n"


def write_report(path: Path, text: str) -> None:
    """Записує текстовий звіт у файл UTF-8 зі стабільним роздільником рядка."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as target:
        target.write(text)
