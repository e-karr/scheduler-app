import pytest


@pytest.fixture
def sample_schedule():
    return {
        "Week 1": [
            {
                "rank_a": 3,
                "name_a": "Global Cafe",
                "rank_b": 4,
                "name_b": "Invictus Fitness",
                "diff": 1,
                "weight": 9,
            },
            {
                "rank_a": 6,
                "name_a": "Lawrence Shirt Factory",
                "rank_b": 10,
                "name_b": "Sacred Sword",
                "diff": 4,
                "weight": 6,
            },
            {
                "rank_a": 9,
                "name_a": "Free State",
                "rank_b": 8,
                "name_b": "Honey Badgers",
                "diff": 1,
                "weight": 9,
            },
            {
                "rank_a": 7,
                "name_a": "JDE",
                "rank_b": 5,
                "name_b": "Red Legs",
                "diff": 2,
                "weight": 8,
            },
            {
                "rank_a": 1,
                "name_a": "Johnny’s",
                "rank_b": 2,
                "name_b": "Post Haus",
                "diff": 1,
                "weight": 9,
            },
        ],
        "Week 2": [
            {
                "rank_a": 3,
                "name_a": "Global Cafe",
                "rank_b": 5,
                "name_b": "Red Legs",
                "diff": 2,
                "weight": 8,
            },
            {
                "rank_a": 7,
                "name_a": "JDE",
                "rank_b": 6,
                "name_b": "Lawrence Shirt Factory",
                "diff": 1,
                "weight": 9,
            },
            {
                "rank_a": 4,
                "name_a": "Invictus Fitness",
                "rank_b": 2,
                "name_b": "Post Haus",
                "diff": 2,
                "weight": 8,
            },
            {
                "rank_a": 9,
                "name_a": "Free State",
                "rank_b": 1,
                "name_b": "Johnny’s",
                "diff": 8,
                "weight": 2,
            },
            {
                "rank_a": 8,
                "name_a": "Honey Badgers",
                "rank_b": 10,
                "name_b": "Sacred Sword",
                "diff": 2,
                "weight": 8,
            },
        ],
        "Week 3": [
            {
                "rank_a": 4,
                "name_a": "Invictus Fitness",
                "rank_b": 1,
                "name_b": "Johnny’s",
                "diff": 3,
                "weight": 7,
            },
            {
                "rank_a": 8,
                "name_a": "Honey Badgers",
                "rank_b": 7,
                "name_b": "JDE",
                "diff": 1,
                "weight": 9,
            },
            {
                "rank_a": 3,
                "name_a": "Global Cafe",
                "rank_b": 2,
                "name_b": "Post Haus",
                "diff": 1,
                "weight": 9,
            },
            {
                "rank_a": 6,
                "name_a": "Lawrence Shirt Factory",
                "rank_b": 5,
                "name_b": "Red Legs",
                "diff": 1,
                "weight": 9,
            },
            {
                "rank_a": 9,
                "name_a": "Free State",
                "rank_b": 10,
                "name_b": "Sacred Sword",
                "diff": 1,
                "weight": 9,
            },
        ],
        "Week 4": [
            {
                "rank_a": 7,
                "name_a": "JDE",
                "rank_b": 10,
                "name_b": "Sacred Sword",
                "diff": 3,
                "weight": 7,
            },
            {
                "rank_a": 9,
                "name_a": "Free State",
                "rank_b": 5,
                "name_b": "Red Legs",
                "diff": 4,
                "weight": 6,
            },
            {
                "rank_a": 8,
                "name_a": "Honey Badgers",
                "rank_b": 4,
                "name_b": "Invictus Fitness",
                "diff": 4,
                "weight": 6,
            },
            {
                "rank_a": 3,
                "name_a": "Global Cafe",
                "rank_b": 1,
                "name_b": "Johnny’s",
                "diff": 2,
                "weight": 8,
            },
            {
                "rank_a": 6,
                "name_a": "Lawrence Shirt Factory",
                "rank_b": 2,
                "name_b": "Post Haus",
                "diff": 4,
                "weight": 6,
            },
        ],
    }


@pytest.fixture
def expected_week_diffs_dict():
    return {"Week 1": 1.8, "Week 2": 3, "Week 3": 1.4, "Week 4": 3.4}


@pytest.fixture
def expected_balance_report(expected_week_diffs_dict):
    return {
        "season_avg_diff": 2.4,
        "week_diffs_dict": expected_week_diffs_dict,
        "parity_score": 0.27,
        "status": "GOOD: Balanced matchups. The weighting is clearly working.",
    }
