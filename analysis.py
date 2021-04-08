import itertools
import math
import concurrent.futures
import random
from gametype import GameType
from profile import Profile
from game import Game
from multiprocessing import Manager


class Analysis:
    def __init__(self, type, profile, quota, expected_outcome=None):
        self.type = type
        self.profile = profile
        self.quota = quota
        self.expected_outcome = expected_outcome

    def outcomes(self):
        """The possible outcomes for the current configuration.

        Currently just loops over all permutations of the agenda, calculates the
        outcome and adds the result to the set of outcomes. This is not very
        efficient, so keep that in mind for larger agendas/profiles!
        """

        outcomes = dict.fromkeys(self.profile.alternatives, 0)
        m = len(self.profile.alternatives)
        n = len(self.profile.ballots)
        permutations = []

        if m > 7:
            # minimum between n^2 and 7!
            # based on doi:10/gdtm7r, section 6.3
            total = min(n**2, 5040)
            for _ in range(total):
                new_perm = list(random.sample(list(self.profile.alternatives), m))
                while new_perm in permutations:
                    new_perm = list(random.sample(list(self.profile.alternatives), m))
                permutations.append(new_perm)
        else:
            permutations = list(itertools.permutations(self.profile.alternatives))
            total = math.factorial(len(self.profile.alternatives))

        print(f"Testing {total} agendas...")

        outcomes_temp = []

        with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
            for permutation in permutations:
                outcomes_temp.append(
                    executor.submit(calculate_outcome, self.type, permutation, self.quota, self.profile)
                )

        for outcome in outcomes_temp:
            result = outcome.result()
            outcomes[result] = outcomes.get(result, 0) + 1

        nonzero_outcomes = list(filter(lambda x: x[1] > 0, outcomes.items()))

        outcome = sorted(
            list(
                map(lambda tup: self.profile.alternative_name(tup[0]), nonzero_outcomes)
            )
        )

        percentage = 0

        if self.expected_outcome != None:
            total = sum(outcomes.values())
            num_expected_outcome = outcomes[self.expected_outcome]
            percentage = num_expected_outcome / total * 100

        return percentage, outcome

def calculate_outcome(type, permutation, quota, profile):
    game = Game(type, list(permutation), quota, profile)
    return game.outcome()
