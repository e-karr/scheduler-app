def generate_balance_report(schedule: dict[str, list[dict]], num_teams: int) -> dict:
    """
    Generates the balance report based on passed season schedule and number of teams.

    Example passed schedule:
    ```python
        {
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
            ]
        }
    ```

    Example balance report:
    ```python
        {
            "season_avg_diff": 2.4,
            "week_diffs_dict": {"Week 1": 1.8, "Week 2": 3, "Week 3": 1.4, "Week 4": 3.4},
            "parity_score": 0.27,
            "status": "GOOD: Balanced matchups. The weighting is clearly working.",
        }
    ```

    :param schedule: Full generated season schedule
    :type schedule: dict[str, list[dict]]
    :param num_teams: Total number of teams
    :type num_teams: int
    :return: Description
    :rtype: dict
    """

    week_diffs_dict = _calc_weekly_averages(schedule)
    total_diff = sum(
        game["diff"] for week_games in schedule.values() for game in week_games
    )
    total_games = sum(len(games) for _, games in schedule.items())
    max_possible_diff = num_teams - 1

    season_avg_diff = total_diff / total_games

    quality_ratio = round(season_avg_diff / max_possible_diff, 2)

    status = _determine_status(quality_ratio)

    balance_report = {
        "season_avg_diff": season_avg_diff,
        "week_diffs_dict": week_diffs_dict,
        "parity_score": quality_ratio,
        "status": status,
    }

    return balance_report


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
        status = "EXCELLENT: Highly competitive. Teams are playing very close seeds."
    elif quality_ratio <= 0.40:
        status = "GOOD: Balanced matchups. The weighting is clearly working."
    elif quality_ratio <= 0.55:
        status = "MODERATE: Fairly spread out. Close to a standard random draw."
    else:
        status = "LOW: High rank disparity. Consider increasing your weight exponent."

    return status


def _calc_weekly_averages(schedule: dict[str, list[dict]]) -> dict[str, float]:
    """
    Calculates the average rank difference for matchups per week. Creates a dictionary with the per week average rank difference

    Example:
    ```python
        {
            "Week 1": 1.8,
            "Week 2": 3,
            "Week 3": 1.4,
            "Week 4": 3.4
        }
    ```

    :param schedule: the full season schedule
    :type schedule: dict[str, list[dict]]
    :return: dictionary of the average rank difference for weekly matchups
    :rtype: dict[str, float]
    """

    week_diffs_dict = {}
    for week_name, games in schedule.items():
        week_diffs = [g["diff"] for g in games]

        avg_week_diff = sum(week_diffs) / len(week_diffs)
        week_diffs_dict[week_name] = avg_week_diff

    return week_diffs_dict
