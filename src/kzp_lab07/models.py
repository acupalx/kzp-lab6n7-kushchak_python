"""Модель матчу варіанта 17 («Спортивна ліга»).

Базовий клас `Match` зберігає спільний стан і перевіряє спільні інваріанти;
`GroupMatch` і `PlayoffMatch` по-різному реалізують `points()` — спільну
операцію нарахування очок. `analysis.py` викликає `points()` через
протокол `PointsEarning`, не перевіряючи конкретний підтип.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Match:
    """Базова сутність матчу зі спільним станом і перевіреними полями."""

    KIND: str = "матч"

    def __init__(
        self,
        home: str,
        away: str,
        date: str,
        home_score: int,
        away_score: int,
        round_number: int,
    ) -> None:
        """Створює матч, перевіряючи спільні інваріанти полів.

        :raises ValueError: якщо назва команди чи дата порожні, або рахунок від'ємний.
        """
        if not home.strip():
            raise ValueError("порожня назва команди господарів")
        if not away.strip():
            raise ValueError("порожня назва команди гостей")
        if not date.strip():
            raise ValueError("порожня дата")
        if home_score < 0 or away_score < 0:
            raise ValueError("рахунок не може бути від'ємним")
        self.home = home
        self.away = away
        self.date = date
        self.home_score = home_score
        self.away_score = away_score
        self.round = round_number  # проходить через setter властивості round

    @property
    def round(self) -> int:
        """Повертає номер туру."""
        return self._round

    @round.setter
    def round(self, value: int) -> None:
        """Встановлює номер туру.

        :raises ValueError: якщо значення менше 1.
        """
        # Внутрішнє поле _round не викликає сам сеттер повторно.
        if value < 1:
            raise ValueError("тур має бути не менше 1")
        self._round = value

    @property
    def kind(self) -> str:
        """Повертає текстову категорію матчу — визначається підтипом через `KIND`."""
        return self.KIND

    def points(self) -> tuple[int, int]:
        """Обчислює очки (господарі, гості) за результатом матчу.

        Базовий клас оголошує контракт; формулу визначає підтип.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """Повертає коротке подання матчу для читача."""
        score = f"{self.home_score}:{self.away_score}"
        return f"{self.home} {score} {self.away} (тур {self.round}, {self.kind})"

    def __repr__(self) -> str:
        """Повертає діагностичне подання матчу з назвою фактичного підтипу."""
        return (
            f"{type(self).__name__}(home={self.home!r}, away={self.away!r}, date={self.date!r}, "
            f"home_score={self.home_score!r}, away_score={self.away_score!r}, round={self.round!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Порівнює матчі за підтипом і значеннями всіх полів."""
        if type(self) is not type(other):
            return NotImplemented
        return (self.home, self.away, self.date, self.home_score, self.away_score, self.round) == (
            other.home,
            other.away,
            other.date,
            other.home_score,
            other.away_score,
            other.round,
        )


class GroupMatch(Match):
    """Матч групового етапу: нічия дозволена."""

    KIND = "група"

    def points(self) -> tuple[int, int]:
        """Нараховує 3 очки за перемогу, 1 за нічию, 0 за поразку."""
        if self.home_score > self.away_score:
            return 3, 0
        if self.home_score < self.away_score:
            return 0, 3
        return 1, 1


class PlayoffMatch(Match):
    """Матч плей-офф: нічия заборонена, переможець отримує 2 очки."""

    KIND = "плей-офф"

    def __init__(
        self,
        home: str,
        away: str,
        date: str,
        home_score: int,
        away_score: int,
        round_number: int,
    ) -> None:
        """Створює матч плей-офф, перевіряючи спільні інваріанти та відсутність нічиєї.

        :raises ValueError: якщо рахунок рівний (нічия в плей-офф неможлива).
        """
        super().__init__(home, away, date, home_score, away_score, round_number)
        if self.home_score == self.away_score:
            raise ValueError("матч плей-офф не може закінчитися нічиєю")

    def points(self) -> tuple[int, int]:
        """Нараховує 2 очки переможцю, 0 переможеному."""
        return (2, 0) if self.home_score > self.away_score else (0, 2)


class PointsEarning(Protocol):
    """Протокол об'єктів, здатних нарахувати очки за результатом матчу.

    `analysis.build_standings` типізується цим протоколом, а не конкретним
    класом `Match` — будь-який об'єкт із цими полями та методом підійде.
    """

    home: str
    away: str
    home_score: int
    away_score: int

    def points(self) -> tuple[int, int]:
        """Повертає очки (господарі, гості) за результатом матчу."""
        ...


@dataclass(frozen=True)
class TeamStanding:
    """Незмінний рядок турнірної таблиці для однієї команди."""

    team: str
    played: int
    points: int
    goal_difference: int
