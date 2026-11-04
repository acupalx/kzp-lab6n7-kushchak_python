"""Формує детермінований текстовий звіт над записами матчів варіанта 17.

Не читає CSV і не знає про аргументи командного рядка — лише перетворює вже
завантажені записи на текст і, за потреби, записує його у файл.
"""

from __future__ import annotations

from pathlib import Path

from kzp_lab06.analysis import build_summary, count_by_round, unique_teams

# Поріг звіту: з якого туру рахуються підсумкові метрики (константа варіанта,
# зафіксована тут і в REPORT.md).
MIN_ROUND = 3


def format_report(records: list[dict[str, object]]) -> str:
    """Форматує підсумок у детермінований текстовий звіт."""
    rounds = count_by_round(records)
    teams = unique_teams(records)
    summary = build_summary(
        records,
        "total_goals",
        "max_difference",
        min_round=MIN_ROUND,
        total_goals="Голів",
        max_difference="Макс. різниця",
    )

    lines = [
        f"Записів: {len(records)}",
        f"Унікальних команд: {len(teams)}",
    ]
    for round_number in sorted(rounds):
        lines.append(f"Тур {round_number}: {rounds[round_number]} матчів")
    lines.append(f"Матчів від туру {MIN_ROUND}: {summary['count']}")
    lines.append(f"Голів від туру {MIN_ROUND}: {summary['Голів']:.2f}")
    lines.append(f"Макс. різниця від туру {MIN_ROUND}: {summary['Макс. різниця']:.2f}")
    return "\n".join(lines) + "\n"


def write_report(path: Path, text: str) -> None:
    """Записує текстовий звіт у файл UTF-8 зі стабільним роздільником рядка.

    Каталог призначення створюється окремо, якщо він ще не існує.
    """
    # with гарантує закриття файла навіть у разі помилки запису.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as target:
        target.write(text)
