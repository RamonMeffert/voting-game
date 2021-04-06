from itertools import permutations
from gametype import GameType
from profile import Profile
from game import Game

class Analysis:
    
    def __init__(self, type, profile, quota, expected_outcome = None):
        self.type = type
        self.profile = profile
        self.quota = quota
        self.expected_outcome = expected_outcome

    def quota_outcomes(self):
        """The possible outcomes for the current configuration.

        Currently just loops over all permutations of the agenda, calculates the
        outcome and adds the result to the set of outcomes. This is not very
        efficient, so keep that in mind for larger agendas/profiles!
        """

        outcomes = dict.fromkeys(self.profile.alternatives, 0)

        for permutation in permutations(self.profile.alternatives):
            game = Game(self.type, list(permutation), self.quota, self.profile)
            outcome = game.outcome()
            # uncomment the line below for debugging
            # print(f"agenda = {list(permutation)}, outcome = {outcome}")
            outcomes[outcome] += 1

        nonzero_outcomes = list(filter(lambda x : x[1] > 0, outcomes.items()))

        outcome = sorted(list(map(lambda tup : self.profile.alternative_name(tup[0]), nonzero_outcomes)))

        if self.expected_outcome != None:
            total = sum(outcomes.values())
            num_expected_outcome = outcomes[self.expected_outcome]
            percentage = num_expected_outcome / total * 100
            print(f"The expected outcome occured {round(percentage, 1)}% ({num_expected_outcome}/{total}) of the time.")

        return outcome