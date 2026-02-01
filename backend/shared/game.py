from dataclasses import dataclass

from shared.team import Team


@dataclass()
class Game:
    """
    A dataclass for storing individual games.

    When comparing Game objects, the team names are sorted alphabetically. If the sorted team names match, then the Game objects are equal. TeamA vs TeamB is the same game as TeamB vs TeamA.

    :param team_a: The first team object
    :type team_a: Team

    :param team_b: The second team object
    :type team_b: Team

    :param game_weight: The weight of the matchup, likelihood to be selected for the week/season
    :type game_weight: float

    :param rank_diff: The diffence in rank for the two teams. Calculated after init.
    :type rank_diff: int
    """

    team_a: Team
    team_b: Team
    game_weight: float
    rank_diff: int = 0

    def __post_init__(self):
        """
        Calculate the rank difference between the teams
        """
        self.rank_diff = abs(self.team_a.rank - self.team_b.rank)

    def __eq__(self, other):
        game_one_teams = sorted([self.team_a.name, self.team_b.name], key=str.lower)
        game_two_teams = sorted([other.team_a.name, other.team_b.name], key=str.lower)

        return game_one_teams == game_two_teams
