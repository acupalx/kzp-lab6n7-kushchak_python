"""Обчислення над типізованими записами матчів варіанта 17 («Спортивна ліга»).

Функції тут лише обчислюють і повертають дані — жодна з них не відкриває
файли й не форматує текст звіту (цим опікується ``reporting.py``).
"""

from __future__ import annotations

from collections.abc import Callable


def matches_in_round(
    records: list[dict[str, object]], round_number: int
) -> list[dict[str, object]]:
    """Повертає матчі заданого туру (запит «відбір» варіанта 17)."""
    return [record for record in records if record["round"] == round_number]


def count_by_round(records: list[dict[str, object]]) -> dict[int, int]:
    """Рахує кількість матчів за туром (запит «словник» варіанта 17).

    Ключі словника відсортовані за зростанням номера туру, щоб текст звіту
    не залежав від порядку рядків у вхідному файлі.
    """
    rounds = {int(record["round"]) for record in records}
    return {
        round_number: sum(1 for record in records if record["round"] == round_number)
        for round_number in sorted(rounds)
    }


def unique_teams(records: list[dict[str, object]]) -> set[str]:
    """Повертає множину всіх команд-господарів і команд-гостей (запит «множина» варіанта 17)."""
    return {str(record["home"]) for record in records} | {str(record["away"]) for record in records}


def _total_goals(rows: list[dict[str, object]]) -> float:
    return float(sum(int(row["home_score"]) + int(row["away_score"]) for row in rows))


def _max_difference(rows: list[dict[str, object]]) -> float:
    return float(
        max((abs(int(row["home_score"]) - int(row["away_score"])) for row in rows), default=0)
    )


_METRIC_FUNCS: dict[str, Callable[[list[dict[str, object]]], float]] = {
    "total_goals": _total_goals,
    "max_difference": _max_difference,
}


def build_summary(
    records: list[dict[str, object]],
    *metrics: str,
    min_round: int = 1,
    **labels: str,
) -> dict[str, object]:
    """Обчислює вибрані метрики для матчів, починаючи із заданого туру.

    Записи з ``round < min_round`` відсіюються один раз, після чого всі
    метрики обчислюються над тим самим відібраним набором ``selected``.
    ``labels`` дозволяє перейменувати ключ результату для кожної метрики
    (наприклад, ``total_goals="Голів"``); типове значення ``min_round=1`` не є
    змінюваним об'єктом і не створює стану між викликами.

    :raises ValueError: якщо передано назву метрики, якої не існує.
    """
    selected = [record for record in records if int(record["round"]) >= min_round]
    result: dict[str, object] = {"count": len(selected)}
    for metric in metrics:
        if metric not in _METRIC_FUNCS:
            raise ValueError(f"Невідома метрика: {metric}")
        result[labels.get(metric, metric)] = _METRIC_FUNCS[metric](selected)
    return result
