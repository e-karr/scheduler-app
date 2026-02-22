from shared.game import Game
from shared.team import Team
import pytest

@pytest.fixture
def teams():
    team1 = Team('Team1', 1)
    team2 = Team('Team2', 2)
    team3 = Team('Team2', 3)
    team4 = Team('Team4', 4)

    return team1, team2, team3, team4

def test_game_post_init(teams):
    team1, team2, team3, team4 = teams
    game1 = Game(team1, team2, 4)
    game2 = Game(team3, team4, 3)
    game3 = Game(team1, team3, 2)

    assert game1.rank_diff == 1
    assert game2.rank_diff == 1
    assert game3.rank_diff == 2

def test_game_eq(teams):
    team1, team2, team3, team4 = teams
    game1 = Game(team1, team2, 4)
    game2 = Game(team3, team4, 3)
    game3 = Game(team2, team1, 2)
    game4 = Game(team3, team4, 1)

    assert game1 != game2
    assert game1 == game3
    assert game2 == game4