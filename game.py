from gametype import GameType

class Game:

    def __init__(self, type, agenda, quota, profile):

        if not set(agenda).issubset(profile.alternatives):
            raise ValueError(
                "The agenda contains alternatives that are not in the profile."
            )

        # The game type, either AMENDMENT or SUCCESSIVE.
        self.type = type

        # The initial agenda.
        self.agenda = agenda

        # The quota, i.e. the number of votes that an alternative has to reach
        # in order for it to win.
        self.quota = quota

        # A profile of voter ballots
        self.profile = profile


    def outcome(self):
        if self.type == GameType.AMENDMENT:
            return self.outcome_amendment(self.agenda)
        else:
            return self.outcome_successive(self.agenda)


    def outcome_amendment(self, agenda):
        """Recursive algorithm for calculating the outcome of the amendment
        procedure for a given agenda. Recursive calls receive a copy of the
        agenda with either the first or second alternative removed, whichever 
        did not reach the quota or was excluded due to tie-breaking.
        """

        if len(agenda) >= 3:
            # If there are at least 3 items, we can modify the agenda and do a
            # recursive call which still has 2 items so we can compare them

            # agenda minus option 2, e.g. [x1, x3, ..., xm]
            left = [agenda[0]] + agenda[2:]
            # agenda minus option 1, e.g. [x2, x3, ..., xm]
            right = agenda[1:]

            # recursively calculate outcomes for both branches
            outcome_left = self.outcome_amendment(left)
            outcome_right = self.outcome_amendment(right)

            # condition: o^A(x1, x3, …, xm) P o^A(x2, x3, …, xm)
            num_prefers_left = self.profile.num_prefers(
                outcome_left, outcome_right)

            # Pick an outcome with tie breaking: if the left branch doesn't win,
            # take the right branch.
            if num_prefers_left >= self.quota:
                return outcome_left
            else:
                return outcome_right

        elif len(agenda) == 2:
            # If there are only two items left, pick the one that reaches the
            # quota (again with tie-breaking)

            num_prefers_left = self.profile.num_prefers(agenda[0], agenda[1])

            if num_prefers_left >= self.quota:
                return agenda[0]
            else:
                return agenda[1]


    def outcome_successive(self, agenda):
        """Recursive algorithm for calculating the outcome of the successive
        procedure for a given agenda. Recursive calls receive a copy of the
        agenda with the first alternative removed.
        """

        if len(agenda) >= 3:
            # If there are at least 3 items, we can modify the agenda and do a
            # recursive call which still has 2 items so we can compare them

            # left is first option in the agenda, e.g. x1
            left = agenda[0]
            # right is rest of the agenda, e.g. [x2, x3, …, xm]
            right = agenda[1:]

            # recursively calculate the outcome of the right branch
            outcome_right = self.outcome_successive(right)

            # condition: x1 P o^S(x2, x3, …, xm)
            num_prefers_left = self.profile.num_prefers(left, outcome_right)

            if num_prefers_left >= self.quota:
                return left
            else:
                return outcome_right

        elif len(agenda) == 2:
            # o^S(x) = x, so when m = 2, x1 P o^S(x2) == x1 P x2
            left = agenda[0]
            right = agenda[1]

            num_prefers_left = self.profile.num_prefers(left, right)

            if num_prefers_left >= self.quota:
                return left
            else:
                return right
