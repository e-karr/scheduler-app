import pytest

from shared.game import Game
from shared.team import Team
from generator_lambda.shared.balance_report import BalanceReport


@pytest.fixture
def sample_schedule():
    return {
        "Week 1": [
            Game(Team("Global Cafe", 3), Team("Invictus Fitness", 4), 9),
            Game(Team("LSF", 6), Team("Sacred Sword", 10), 6),
            Game(Team("Free State", 9), Team("Honey Badgers", 8), 9),
            Game(Team("JDE", 7), Team("Red Legs", 5), 8),
            Game(Team("Johnny’s", 1), Team("Post Haus", 2), 9),
        ],
        "Week 2": [
            Game(Team("Global Cafe", 3), Team("Red Legs", 5), 8),
            Game(Team("JDE", 7), Team("LSF", 6), 9),
            Game(Team("Invictus Fitness", 4), Team("Post Haus", 2), 8),
            Game(Team("Free State", 9), Team("Johnny’s", 1), 2),
            Game(Team("Honey Badgers", 8), Team("Sacred Sword", 10), 8),
        ],
        "Week 3": [
            Game(Team("Invictus Fitness", 4), Team("Johnny’s", 1), 7),
            Game(Team("Honey Badgers", 8), Team("JDE", 7), 9),
            Game(Team("Global Cafe", 3), Team("Post Haus", 2), 9),
            Game(Team("LSF", 6), Team("Red Legs", 5), 9),
            Game(Team("Free State", 9), Team("Sacred Sword", 10), 9),
        ],
        "Week 4": [
            Game(Team("JDE", 7), Team("Sacred Sword", 10), 7),
            Game(Team("Free State", 9), Team("Red Legs", 5), 6),
            Game(Team("Honey Badgers", 8), Team("Invictus Fitness", 4), 6),
            Game(Team("Global Cafe", 3), Team("Johnny’s", 1), 8),
            Game(Team("LSF", 6), Team("Post Haus", 2), 6),
        ],
    }


@pytest.fixture
def expected_week_diffs_dict():
    return {"Week 1": 1.8, "Week 2": 3, "Week 3": 1.4, "Week 4": 3.4}


@pytest.fixture
def expected_balance_report(expected_week_diffs_dict):
    return BalanceReport(2.4, expected_week_diffs_dict, 0.27, "GOOD")
