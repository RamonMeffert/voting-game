from enum import Enum

class Rule(Enum):
    PLURALITY = 1,
    BORDA = 2,
    CONDORCET = 3,
    WEAK_CONDORCET = 4


    # magic methods for argparse compatibility

    def __str__(self):
        return str.lower(self.name)

    def __repr__(self):
        return str(self)

    @staticmethod
    def argparse(s):
        try:
            return Rule[s.upper()]
        except KeyError:
            return s
