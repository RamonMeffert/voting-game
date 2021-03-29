from enum import Enum

class GameType(Enum):
    AMENDMENT = 1,
    SUCCESSIVE = 2

class Game:

    def __init__(self, game_type, agenda, quota, profile):
        self.game_type = game_type
        self.agenda    = agenda
        self.quota     = quota
        self.profile   = profile

    def outcome(self):
        if self.game_type == GameType.AMENDMENT:
            return self.outcome_amendment(self.agenda)
        else:
            return self.outcome_successive(self.agenda)

    def outcome_amendment(self, agenda):

        if len(agenda) >= 3:
            # agenda minus option x2
            new_agenda_left = [agenda[0]] + agenda[2:]
            # agenda minus option x1
            new_agenda_right = agenda[1:]

            outcome_1_3 = self.outcome_amendment(new_agenda_left)
            outcome_2_3 = self.outcome_amendment(new_agenda_right)

            num_prefers_left = self.profile.num_prefers(outcome_1_3, outcome_2_3)
            
            
            if num_prefers_left >= self.quota:
                return outcome_1_3
            else:
                return outcome_2_3

        elif len(agenda) == 2:
            num_prefers_left = self.profile.num_prefers(agenda[0], agenda[1])

            if num_prefers_left >= self.quota:
                return agenda[0]
            else:
                return agenda[1]

    def outcome_successive(self, agenda):
        pass