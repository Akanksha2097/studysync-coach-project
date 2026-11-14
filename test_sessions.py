from datetime import date

from sessions import SessionDC, find_conflicts, next_occurrence


def test_dataclass_and_recurring_dates():
    assert SessionDC("Math", 30).priority == "medium"
    assert next_occurrence(date(2026, 1, 1), "weekly") == date(2026, 1, 8)


def test_conflict_detection_is_pairwise_and_safe_on_empty_input():
    sessions = [{"subject": "Math", "slot": "08:00"}, {"subject": "Chem", "slot": "08:00"}, {"subject": "Art", "slot": "09:00"}]
    assert len(find_conflicts(sessions)) == 1
    assert find_conflicts([]) == []
