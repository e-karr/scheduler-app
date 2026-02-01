from dataclasses import dataclass
from shared.game import Game


@dataclass
class BalanceReport:
    """
    Data class representing the final season Balance Report

    :param season_avg_diff: The average rank difference in matchups for the whole season
    :type season_avg_diff: float
    :param week_diff_dict: A dictionary of the week by week average mathcup rank difference
    :type week_diff_dict: dict[str, float]
    :param parity_score: Ratio representing how closely matched the season matchups are
    :type parity_score: float
    :param quality_status: Status for how balanced the season is
    :type quality_status: str
    """

    season_avg_diff: float
    week_diff_dict: dict[str, float]
    parity_score: float
    quality_status: str


def generate_balance_report(
    schedule: dict[str, list[Game]], num_teams: int
) -> BalanceReport:
    """
    Generates the balance report based on passed season schedule and number of teams.

    Example passed schedule:
    ```python
        {
            "Week 1": [
                Game(Team('Global Cafe', 3), Team('Invictus Fitness', 4), 9),
                Game(Team('LSF', 6), Team('Sacred Sword', 10), 6),
                Game(Team('Free State', 9), Team('Honey Badgers', 8), 9),
                Game(Team('JDE', 7), Team('Red Legs', 5), 8),
                Game(Team('Johnny’s', 1), Team('Post Haus', 2), 9)
            ],
            "Week 2": [
                Game(Team('Global Cafe', 3), Team('Red Legs', 5), 8),
                Game(Team('JDE', 7), Team('LSF', 6), 9),
                Game(Team('Invictus Fitness', 4), Team('Post Haus', 2), 8),
                Game(Team('Free State', 9), Team('Johnny’s', 1), 2),
                Game(Team('Honey Badgers', 8), Team('Sacred Sword', 10), 8)
            ]
        }
    ```

    Example balance report:
    ```python
        BalanceReport(
            2.4,
            {
                "Week 1": 1.8,
                "Week 2": 3,
                "Week 3": 1.4,
                "Week 4": 3.4
            },
            0.27,
            "GOOD"
        )
    ```

    :param schedule: Full generated season schedule
    :type schedule: dict[str, list[Game]]
    :param num_teams: Total number of teams
    :type num_teams: int
    :return: The season balance report detailing the season average rank differance, the week by week average rank difference, parity score, and balance status
    :rtype: BalanceReport
    """

    week_diffs_dict = {
        week: _calc_weekly_average(games) for week, games in schedule.items()
    }

    total_diff = sum(
        game.rank_diff for week_games in schedule.values() for game in week_games
    )
    total_games = sum(len(games) for _, games in schedule.items())
    max_possible_diff = num_teams - 1

    season_avg_diff = total_diff / total_games

    quality_ratio = round(season_avg_diff / max_possible_diff, 2)

    status = _determine_status(quality_ratio)

    return BalanceReport(season_avg_diff, week_diffs_dict, quality_ratio, status)


def _determine_status(quality_ratio: float) -> str:
    """
    Returns the status for season parity based on the quality ratio.

    - ratio <= .25 is EXCELLENT
    - ratio > .25 and <= .40 is GOOD
    - ratio > .40 and <= .55 is MODERATE
    - ratio > .55 is LOW

    :param quality_ratio: Season parity score: `season_avg_rank_diff / max_possible_dif`
    :type quality_ratio: float

    :return: Status detailing if the season has good parity
    :rtype: str
    """
    if quality_ratio <= 0.25:
        status = "EXCELLENT"
    elif quality_ratio <= 0.40:
        status = "GOOD"
    elif quality_ratio <= 0.55:
        status = "MODERATE"
    else:
        status = "LOW"

    return status


def _calc_weekly_average(games: list[Game]) -> float:
    """
    Calculates the average rank difference for Games in a week.

    :param games: List of Games played in a week
    :type games: list[Game]
    :return: dictionary of the average rank difference for weekly matchups
    :rtype: float
    """

    week_diffs = [g.rank_diff for g in games]

    avg_week_diff = sum(week_diffs) / len(week_diffs)

    return avg_week_diff
