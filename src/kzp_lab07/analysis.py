"""Обчислення над об'єктами `Match`.

`matches_in_round`, `count_by_round`, `unique_teams`, `total_goals` і
`max_score_difference` переносять ту саму логіку й ті самі формули, що
працювали над словниками в лаб. 6, тепер через атрибути об'єктів —
еквівалентність перевірена тестом `test_legacy_equivalence.py` на тих самих
восьми матчах групового етапу. `build_standings` — нова турнірна таблиця:
жодна функція тут не перевіряє конкретний підтип матчу через `isinstance`.
"""

from __future__ import annotations

from collections.abc import Iterable

from kzp_lab07.models import Match, PointsEarning, TeamStanding


def matches_in_round(matches: list[Match], round_number: int) -> list[Match]:
    """Повертає матчі заданого туру."""
    return [match for match in matches if match.round == round_number]


def count_by_round(matches: list[Match]) -> dict[int, int]:
    """Рахує кількість матчів за туром; ключі відсортовані за зростанням."""
    rounds = {match.round for match in matches}
    return {
        round_number: sum(1 for match in matches if match.round == round_number)
        for round_number in sorted(rounds)
    }


def unique_teams(matches: list[Match]) -> set[str]:
    """Повертає множину всіх команд-господарів і команд-гостей."""
    return {match.home for match in matches} | {match.away for match in matches}


def total_goals(matches: list[Match]) -> float:
    """Сумарна кількість голів усіх матчів."""
    return float(sum(match.home_score + match.away_score for match in matches))


def max_score_difference(matches: list[Match]) -> float:
    """Найбільша різниця рахунку серед матчів."""
    return float(max((abs(match.home_score - match.away_score) for match in matches), default=0))


def build_standings(matches: Iterable[PointsEarning]) -> list[TeamStanding]:
    """Будує турнірну таблицю: очки й різницю голів за командою.

    Кожен матч сам визначає, скільки очок отримує кожна команда, через
    `points()` — ця функція працює з будь-яким об'єктом протоколу
    `PointsEarning`, не перевіряючи конкретний клас.

    Рядки впорядковані за спаданням очок, потім різниці голів, потім за
    назвою команди — для детермінованого звіту.
    """
    played: dict[str, int] = {}
    points: dict[str, int] = {}
    goals_for: dict[str, int] = {}
    goals_against: dict[str, int] = {}

    for match in matches:
        home_points, away_points = match.points()
        for team, scored, conceded, earned in (
            (match.home, match.home_score, match.away_score, home_points),
            (match.away, match.away_score, match.home_score, away_points),
        ):
            played[team] = played.get(team, 0) + 1
            points[team] = points.get(team, 0) + earned
            goals_for[team] = goals_for.get(team, 0) + scored
            goals_against[team] = goals_against.get(team, 0) + conceded

    standings = [
        TeamStanding(
            team=team,
            played=played[team],
            points=points[team],
            goal_difference=goals_for[team] - goals_against[team],
        )
        for team in played
    ]
    standings.sort(key=lambda row: (-row.points, -row.goal_difference, row.team))
    return standings
