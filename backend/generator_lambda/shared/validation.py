
class RepeatMatchupError(Exception):
    """
    Exception raised if repeat matchup is found.
    """

    def __init__(self, repeat_matchup):
        super().__init__(f'Repeat matchup found: {repeat_matchup}')



def validate_full_schedule(schedule: dict[str, list[dict]], num_teams: int) -> bool:
    all_checks_passed = False
    correct_num_games = False
    one_game_per_week = False

    # Track all matchups to check for repeats
    master_matchup_tracker = set()

    try:

        for week, games in schedule.items():
            teams_this_week = []
            # Check 1: correct number of games
            correct_num_games = len(games) == (num_teams // 2)

            # Check 2: No repeat matchups
            for game in games:

                check_repeat_matchups(master_matchup_tracker, game)

                teams_this_week.extend([game['name_a'], game['name_b']])

            # Check 3: Every team has one game per week
            one_game_per_week = len(set(teams_this_week)) == num_teams

        all_checks_passed = correct_num_games == one_game_per_week

        return all_checks_passed
    
    except Exception as e:
        raise e
    
def check_repeat_matchups(tracker: set, game: dict) -> None:

    matchup = tuple(sorted([game['name_a'], game['name_b']]))

    if matchup in tracker:
        raise RepeatMatchupError(matchup)
    
    tracker.add(matchup)


    