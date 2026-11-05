# Спортивна ліга — обробка даних засобами Python

Лабораторні роботи № 6-7 з курсу «Кросплатформні засоби програмування».
Варіант 17.

## Призначення

Пакет `kzp_lab06` читає CSV-файл результатів матчів, перетворює текстові
поля на типізовані значення, обчислює показники за списками, словниками й
множинами та записує детермінований текстовий звіт.

## Формат входу

Один запис — рядок CSV, поля розділені комою, файл у кодуванні UTF-8:

```
home,away,date,home_score,away_score,round
```

| Поле | Тип | Опис |
|---|---|---|
| `home` | `str` | команда господарів |
| `away` | `str` | команда гостей |
| `date` | `str` | дата матчу (`YYYY-MM-DD`) |
| `home_score` | `int` | голи господарів |
| `away_score` | `int` | голи гостей |
| `round` | `int` | номер туру (не менше 1) |

Приклад (кома в назві команди екранується лапками, як і повертається назад
`csv.DictReader`):

```
"Карпати, Львів",Верес,2026-03-02,1,1,1
```

## Структура пакета

```
src/kzp_lab06/
├── __init__.py      # публічний мінімальний API
├── errors.py         # DataError
├── loader.py         # читання CSV і перетворення типів
├── analysis.py        # відбір, словник, множина, build_summary
├── reporting.py       # формування й запис текстового звіту
└── cli.py             # аргументи командного рядка й межа помилок
tests/                  # тести pytest
data/input.csv          # контрольний набір варіанта 17
```

## Встановлення та запуск

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"

python -m pytest
ruff check .
ruff format --check .

python -m kzp_lab06.cli data/input.csv reports/summary.txt
# або, якщо пакет встановлено:
kzp-lab06 data/input.csv reports/summary.txt
```

CLI повертає `0` після успіху, `1` для помилки даних чи файлової системи,
`2` для неправильної кількості аргументів.

## Об'єктна модель (лабораторна робота № 7)

Пакет `kzp_lab07` перебудовує лаб. 6 на об'єкти: той самий домен і ті самі
показники (`total_goals`, `max_score_difference`, `count_by_round`,
`unique_teams` — тепер через атрибути об'єктів, а не ключі словника;
еквівалентність зі старими числами доведена тестом
`tests/test_legacy_equivalence.py`), плюс нова турнірна таблиця.

Формат входу розширено одним полем відносно лаб. 6 — `kind` (`group` або
`playoff`), за яким `loader` обирає підтип:

```
home,away,date,home_score,away_score,round,kind
```

```
src/kzp_lab07/
├── __init__.py       # публічний API
├── errors.py          # DataError
├── models.py           # Match (@property round, __str__/__repr__/__eq__),
│                         GroupMatch/PlayoffMatch, Protocol PointsEarning, TeamStanding
├── loader.py            # CSV -> об'єкти відповідного підтипу
├── analysis.py           # перенесені показники лаб. 6 + build_standings
├── reporting.py           # текстовий звіт із турнірною таблицею
└── cli.py                 # той самий контракт CLI, що й у лаб. 6
data/matches.csv          # контрольний набір: 8 матчів групи (ті самі, що в лаб. 6) + 2 плей-офф
```

`Match` — базовий клас зі спільним станом і властивістю `round` (setter
відхиляє значення менше 1). `GroupMatch` (нічия дозволена, очки 3/1/0) і
`PlayoffMatch` (нічия заборонена, переможець отримує 2 очки) по-різному
реалізують `points()` — єдину спільну операцію, яку викликає
`analysis.build_standings` через протокол `PointsEarning`, не перевіряючи
конкретний підтип.

```bash
python -m kzp_lab07.cli data/matches.csv reports/standings.txt
# або, якщо пакет встановлено:
kzp-lab07 data/matches.csv reports/standings.txt
```
