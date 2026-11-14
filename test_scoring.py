from scoring import session_rating
from scoring_helpers import apply_streak_bonus


def test_session_rating_boundaries():
    assert session_rating(49) == "Skip"
    assert session_rating(50) == "Meh"
    assert session_rating(80) == "Good"
    assert session_rating(90) == "Great"


def test_session_rating_rejects_scores_outside_display_range():
    assert session_rating(-1) == "Invalid"
    assert session_rating(101) == "Invalid"


def test_streak_bonus_caps_at_100_and_rejects_raw_input_outside_slider_range():
    assert apply_streak_bonus(90, 10) == 100
    assert apply_streak_bonus(60, 3) == 66
    try:
        apply_streak_bonus(121, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("out-of-range score should raise ValueError")
