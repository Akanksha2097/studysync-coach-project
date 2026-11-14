from ranking import load_study_spots, rank_study_spots, score_study_spot


def test_ranking_loads_typed_csv_and_explains_score():
    spots = load_study_spots("data/study_spots.csv")
    assert isinstance(spots[0]["distance_miles"], float)
    score, reasons = score_study_spot({"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}, spots[0])
    assert score == 7
    assert "quiet enough" in reasons


def test_ranking_returns_top_k_descending():
    spots = load_study_spots("data/study_spots.csv")
    ranked = rank_study_spots({"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}, spots, k=3)
    assert len(ranked) == 3
    assert ranked[0][1] >= ranked[1][1] >= ranked[2][1]
