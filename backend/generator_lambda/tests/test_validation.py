from generator_lambda.shared.validation import (
    check_repeat_matchups,
    check_num_weekly_games,
    check_teams_per_week,
    validate_full_schedule,
)
import pytest
from shared.game import Game
from shared.team import Team


@pytest.mark.parametrize(
    "schedule, expected_result",
    [
        (
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [
                    Game(Team("Team3", 3), Team("Team2", 2), 3),
                    Game(Team("Team1", 1), Team("Team4", 4), 4),
                ],
            },
            True,
        ),
        (
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [
                    Game(Team("Team1", 1), Team("Team2", 2), 3),
                    Game(Team("Team1", 1), Team("Team4", 4), 4),
                ],
            },
            False,
        ),
    ],
)
def test_check_repeat_matchups(schedule, expected_result):
    result = check_repeat_matchups(schedule)

    assert result == expected_result


@pytest.mark.parametrize(
    "schedule, num_teams, expected_result",
    [
        (
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [
                    Game(Team("Team3", 3), Team("Team2", 2), 3),
                    Game(Team("Team1", 1), Team("Team4", 4), 4),
                ],
            },
            4,
            True,
        ),
        (
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [Game(Team("Team1", 1), Team("Team3", 3), 3)],
            },
            4,
            False,
        ),
    ],
)
def test_check_num_weekly_games(schedule, num_teams, expected_result):
    result = check_num_weekly_games(schedule, num_teams)

    assert result == expected_result


@pytest.mark.parametrize(
    "schedule, num_teams, expected_result",
    [
        (
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [
                    Game(Team("Team3", 3), Team("Team2", 2), 3),
                    Game(Team("Team1", 1), Team("Team4", 4), 4),
                ],
            },
            4,
            True,
        ),
        (
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [
                    Game(Team("Team1", 1), Team("Team3", 3), 3),
                    Game(Team("Team1", 1), Team("Team4", 4), 4),
                ],
            },
            4,
            False,
        ),
    ],
)
def test_check_teams_per_week(schedule, num_teams, expected_result):
    result = check_teams_per_week(schedule, num_teams)

    assert result == expected_result


@pytest.mark.parametrize(
    "schedule, num_teams, expected_result",
    [
        (  # Valid schedule
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [
                    Game(Team("Team3", 3), Team("Team2", 2), 3),
                    Game(Team("Team1", 1), Team("Team4", 4), 4),
                ],
            },
            4,
            True,
        ),
        (  # Team2 doesn't have a game in Week 2
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [
                    Game(Team("Team1", 1), Team("Team3", 3), 3),
                    Game(Team("Team1", 1), Team("Team4", 4), 4),
                ],
            },
            4,
            False,
        ),
        (  # Incorrect number of games in Week 2
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [Game(Team("Team1", 1), Team("Team3", 3), 3)],
            },
            4,
            False,
        ),
        (  # Repeat matchup in Week 2
            {
                "Week 1": [
                    Game(Team("Team1", 1), Team("Team2", 2), 1),
                    Game(Team("Team3", 3), Team("Team4", 4), 2),
                ],
                "Week 2": [
                    Game(Team("Team1", 1), Team("Team2", 2), 3),
                    Game(Team("Team1", 1), Team("Team4", 4), 4),
                ],
            },
            4,
            False,
        ),
    ],
)
def test_validate_full_schedule(schedule, num_teams, expected_result):
    result = validate_full_schedule(schedule, num_teams)

    assert result == expected_result
