from enum import Enum

class Rule(Enum):
    PLURALITY = 1,
    BORDA = 2,
    CONDORCET = 3,
    WEAK_CONDORCET = 4