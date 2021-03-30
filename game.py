from enum import Enum

class GameType(Enum):
    AMENDMENT = 1,
    SUCCESSIVE = 2

class Game:

    def __init__(self, game_type, agenda, quota, profile):
        # The game type, either AMENDMENT or SUCCESSIVE.
        self.game_type = game_type
        
        # The initial agenda.
        self.agenda    = agenda
        
        # The quota, i.e. the number of votes that an alternative has to reach
        # in order for it to win.
        self.quota     = quota

        # A profile of voter ballots
        self.profile   = profile

    def outcome(self):
        if self.game_type == GameType.AMENDMENT:
            return self.outcome_amendment(self.agenda)
        else:
            return self.outcome_successive(self.agenda)

    def outcome_amendment(self, agenda):
        """Recursive algorithm for calculating the outcome of the amendment
        procedure for a given agenda. Recursive calls receive a copy of the
        agenda with either the first or second alternative removed, whichever 
        did not reach the quota or was excluded due to tie-breaking.

        Args:
            agenda ([type]): [description]

        Returns:
            [type]: [description]
        """

        if len(agenda) >= 3:
            # If there are at least 3 items, we can modify the agenda and do a
            # recursive call

            # agenda minus option 2, i.e. [x1, x3, ..., xm]
            new_agenda_left = [agenda[0]] + agenda[2:]
            # agenda minus option 1, i.e. [x2, x3, ..., xm]
            new_agenda_right = agenda[1:]

            # calculate outcomes for both agendas
            outcome_1_3 = self.outcome_amendment(new_agenda_left)
            outcome_2_3 = self.outcome_amendment(new_agenda_right)

            # condition: o^A(x1, x3, …, xm) P o^A(x2, x3, …, xm)
            num_prefers_left = self.profile.num_prefers(outcome_1_3, outcome_2_3)
            
            # Pick an outcome with tie breaking: if the left branch doesn't win,
            # take the right branch.
            if num_prefers_left >= self.quota:
                return outcome_1_3
            else:
                return outcome_2_3

        elif len(agenda) == 2:
            # If there are only two items left, pick the one that reaches the
            # quota (again with tie-breaking)

            num_prefers_left = self.profile.num_prefers(agenda[0], agenda[1])

            if num_prefers_left >= self.quota:
                return agenda[0]
            else:
                return agenda[1]

    def outcome_successive(self, agenda):
        pass