"""Доказ еквівалентності: ті самі 8 матчів групового етапу, що й у лаб. 6,
дають ті самі числа через новий об'єктний конвеєр (lab07), що й словниковий
конвеєр лаб. 6 (`tests/test_analysis.py`, `tests/test_reporting.py`).
"""

from __future__ import annotations

from pathlib import Path

from kzp_lab07.analysis import count_by_round, max_score_difference, total_goals, unique_teams
from kzp_lab07.loader import load_matches

# Побудовано з тих самих 8 рядків, що й data/input.csv лаб. 6, лише з доданим kind=group.
LAB06_GROUP_STAGE_CSV = """home,away,date,home_score,away_score,round,kind
Динамо,Шахтар,2026-03-01,3,0,1,group
"Карпати, Львів",Верес,2026-03-02,1,1,1,group
Зоря,Металіст,2026-03-08,2,2,2,group
Оболонь,Полісся,2026-03-09,4,1,2,group
Рух,Колос,2026-03-15,0,3,3,group
Динамо,Шахтар,2026-03-22,1,1,4,group
Верес,"Карпати, Львів",2026-03-23,0,0,4,group
Шахтар,Зоря,2026-03-30,5,2,5,group
"""


def test_group_stage_metrics_match_lab06_dict_based_results(tmp_path: Path) -> None:
    path = tmp_path / "group_stage.csv"
    path.write_text(LAB06_GROUP_STAGE_CSV, encoding="utf-8")

    matches = load_matches(path)

    # Ті самі значення, що й у REPORT.md/тестах лаб. 6 для цього самого набору.
    assert total_goals(matches) == 26.0
    assert max_score_difference(matches) == 3.0
    assert count_by_round(matches) == {1: 2, 2: 2, 3: 1, 4: 2, 5: 1}
    assert len(unique_teams(matches)) == 10
