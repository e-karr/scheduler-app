from shared.game import Game


def validate_full_schedule(schedule: dict[str, list[Game]], num_teams: int) -> bool:
    """
    Validates the full season schedule. To be a valid schedule,
    it must meet these requirements:

    1. Correct number of games per week (total num teams / 2)
    2. No repeat matchups
    3. Every team has one game per week

    :param schedule: The full season schedule
    :type schedule: dict[str, list[Game]]
    :param num_teams: The total number of teams in the league
    :type num_teams: int

    :return: True/False if the schedule is valid
    :rtype: bool
    """

    try:
        # Check 1: Correct number of games per week
        correct_num_games = check_num_weekly_games(schedule, num_teams)

        # Check 2: No repeat matchups
        no_repeats = check_repeat_matchups(schedule)

        # Check 3: Every team has one game per week
        one_game_per_week = check_teams_per_week(schedule, num_teams)

        # All checks pass
        all_checks_passed = correct_num_games == no_repeats == one_game_per_week

        return all_checks_passed

    except Exception as e:
        raise e


def check_repeat_matchups(schedule: dict[str, list[Game]]) -> bool:
    """
    Check for no repeat matchups in a season

    :param schedule: The full season schedule
    :type schedule: dict[str, list[Game]]

    :return: True/False if there are repeat matchups
    :rtype: bool
    """
    all_games = [game for games in schedule.values() for game in games]

    return len(all_games) == len(set(all_games))


def check_num_weekly_games(schedule: dict[str, list[Game]], num_teams: int) -> bool:
    """
    Checks that each week in a schedule has the
    correct number of games.

    :param schedule: The full season schedule
    :type schedule: dict[str, list[Game]]

    :return: True/False if there are the correct number
    of games per week
    :rtype: bool
    """
    correct_num = {len(games) == (num_teams // 2) for _, games in schedule.items()}

    return len(correct_num) == 1 and True in correct_num


def check_teams_per_week(schedule: dict[str, list[Game]], num_teams: int) -> bool:
    """
    Checks that each team has one game per week.

    :param schedule: The full season schedule
    :type schedule: dict[str, list[Game]]

    :return: True/False if each team has one game
    per week
    :rtype: bool
    """

    one_game_per_week = set()

    for _, games in schedule.items():
        teams_this_week = set()

        for game in games:
            teams_this_week.add(game.team_a)
            teams_this_week.add(game.team_b)

        one_game_per_week.add(len(teams_this_week) == num_teams)

    return len(one_game_per_week) == 1 and True in one_game_per_week
