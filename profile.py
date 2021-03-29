import csv

class Profile:
    def __init__(self):
        
        csv.register_dialect("ignore_whitespace", delimiter=",",
                     skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)

        # A ballot is a key-value pair where the key is the voter id and the
        # value is an ordered list of alternatives
        self.ballots = {}

    @staticmethod
    def from_csv(path: str) -> 'Profile':
        """Converts a csv file containing a profile to a Profile object.
        Expects voter ids as column names and preferences as columns, e.g.:

        ```
        1, 2, 3
        a, c, a
        b, a, c
        c, b, b
        ```

        You can imagine this as a profile, but rotated by 90° clockwise.
        Whitespace is ignored.

        Returns:
            Profile: A profile object.
        """
        new_profile = Profile()

        with open(path) as csvfile:
            reader = csv.DictReader(csvfile, dialect="ignore_whitespace")

            for voter in reader.fieldnames:
                new_profile.ballots[int(voter)] = []

            for line in reader:
                for voter in reader.fieldnames:
                    new_profile.ballots[int(voter)].append(line[voter])

        return new_profile

    @staticmethod
    def from_txt(path: str) -> 'Profile':
        """Converts a file containing a profile to a Profile object.
        Expects the following format:

        ```
        1: a b c
        2: c b a
        3: a c b
        ```

        Whitespace is ignored.

        Returns:
            Profile: A profile object.
        """
        new_profile = Profile()

        with open(path) as txtfile:
            reader = txtfile.readlines()

            for voter in reader:
                split = voter.split(":", 1)
                voter_id = int(split[0])
                preference = split[1].split()
                new_profile.ballots[voter_id] = preference

        return new_profile

    def ballot(self, id):
        return self.ballots[id]

    def prefers(self, id, a1, a2) -> bool:
        """Whether a voter with id `id` prefers alternative `a1` over `a2`.
        """

        pref = self.ballot(id)

        # lower index means higher ranking
        return pref.index(a1) < pref.index(a2)

    def num_prefers(self, a1, a2):
        num = 0

        for voter in self.ballots.keys():
            if self.prefers(voter, a1, a2):
                num += 1

        return num