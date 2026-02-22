from dataclasses import dataclass


@dataclass()
class Team:
    """
    A dataclass to store team name and rank.

    When comparing Team objects, only Team.name (lower-case) is compared.

    :param name: The team's name
    :type name: str

    :param rank: The team's rank
    :type rank: int
    """

    name: str
    rank: int

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()
    
    def __hash__(self) -> int:
        return hash(self.name.lower())
