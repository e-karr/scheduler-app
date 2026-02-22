from shared.team import Team

def test_team_eq():
    team1 = Team('Team1', 1)
    team2 = Team('Team2', 2)
    team3 = Team('Team2', 3)

    assert team1 != team2
    assert team2 == team3