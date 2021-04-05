class Ballot:
    def __init__(self, id, preference = [], weight = 1) -> None:
        self.id = id
        self.preference = preference
        self.weight = weight