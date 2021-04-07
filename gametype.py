from enum import Enum


class GameType(Enum):
    AMENDMENT = 1,
    SUCCESSIVE = 2

    # magic methods for argparse compatibility

    def __str__(self):
        return str.lower(self.name)

    def __repr__(self):
        return str(self)

    @staticmethod
    def argparse(s):
        try:
            return GameType[s.upper()]
        except KeyError:
            return s

