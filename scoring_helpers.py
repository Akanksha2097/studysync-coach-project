"""
Target file for Tinker 1B, Part 2.

Move `apply_streak_bonus(combined_score, streak_days)` here from scoring.py,
then update the import at the top of scoring.py so `run_demo()` and the
Session Scorer tab still work exactly as before.
"""

def apply_streak_bonus(combined_score: int, streak_days: int) -> int:
    """Add a bonus for consecutive study days, capped at 100.

    Raises ValueError if combined_score is outside the real 0-120 range
    (two 0-60 sliders) -- catching bad raw input here, before the bonus
    and cap can silently disguise it as a normal-looking score.
    """
    if combined_score < 0 or combined_score > 120:
        raise ValueError(f"combined_score out of range: {combined_score}")
    boosted = combined_score + streak_days * 2
    return min(boosted, 100)


