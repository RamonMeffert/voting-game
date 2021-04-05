from itertools import permutations
from gametype import GameType
from profile import Profile
from game import Game

class Analysis:
    
    def __init__(self, type, profile, quota):
        self.type = type
        self.profile = profile
        self.quota = quota

    def quota_outcomes(self):
        """The possible outcomes for the current configuration.

        Currently just loops over all permutations of the agenda, calculates the
        outcome and adds the result to the set of outcomes. This is not very
        efficient, so keep that in mind for larger agendas/profiles!
        """

        outcomes = set()

        for permutation in permutations(self.profile.alternatives):
            game = Game(self.type, list(permutation), self.quota, self.profile)
            outcome = game.outcome()
            # uncomment the line below for debugging
            # print(f"agenda = {list(permutation)}, outcome = {outcome}")
            outcomes.add(outcome)

        return sorted(list(outcomes))