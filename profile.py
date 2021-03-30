import csv
from typing import Set


class Profile:
    def __init__(self):

        # Register a CSV dialect. Is this the right place to do this?
        # No clue. But I want to be sure my dialect exists so this at least
        # ensures that I guess.
        csv.register_dialect("ignore_whitespace", delimiter=",",
                             skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)

        # A ballot is a key-value pair where the key is the voter id and the
        # value is an ordered list of alternatives
        self.ballots = {}

        # Save the available alternatives as a set
        self.alternatives = set()

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

        # This will raise an error if the profile is invalid
        new_profile.__validate()

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

        # This will raise an error if the profile is invalid
        new_profile.__validate()

        return new_profile

    def __validate(self):
        """Validates the profile by:

        * Checking the length of all ballots is the same
        * Checking if the set of alternatives is the same for all ballots
        """

        # Retrieve the first ballot and take the alternatives in there as the
        # available alternatives
        first_voter_id = next(iter(self.ballots))

        # update(list) on a Set adds all items in that list to the set
        self.alternatives.update(self.ballots.get(first_voter_id))

        # iterate over voter preferences
        # (self.ballots.values() is a list of lists of alternatives)
        for voter, preferences in self.ballots.items():
            # if a ballot has a different number of alternatives than are
            # available, or if it contains alternatives not in the set of
            # alternatives, throw an error
            length_different = len(preferences) != len(self.alternatives)
            alternatives_differ = set(
                preferences).difference(self.alternatives)

            # Provide helpful error message
            if len(alternatives_differ) != 0:
                if length_different:
                    # Different length _and_ different composition
                    raise ValueError(f"\n\tVoter {voter} has a different set "
                                     "of alternatives than I was expecting. I was expecting "
                                     f"{len(self.alternatives)} alternatives but got "
                                     f"{len(preferences)} instead.\n\tAlso, these alternatives "
                                     f"do not appear in the first ballot: {alternatives_differ}.")
                else:
                    # Only different composition
                    raise ValueError(f"\n\tVoter {voter} has a different set "
                                     "of alternatives than I was expecting. These alternatives "
                                     f"do not appear in the first ballot: {alternatives_differ}.")
            elif length_different:
                raise ValueError(f"\n\tVoter {voter} has a different set "
                                 "of alternatives than I was expecting. I was expecting "
                                 f"{len(self.alternatives)} alternatives but got "
                                 f"{len(preferences)} instead.")

    def ballot(self, id):
        """Returns the ballot of a voter with id `id`.

        Returns:
            [type]: [description]
        """
        return self.ballots[id]

    def prefers(self, id, a1, a2) -> bool:
        """Whether a voter with id `id` prefers alternative `a1` over `a2`.
        """

        pref = self.ballot(id)

        # lower index means higher ranking
        return pref.index(a1) < pref.index(a2)

    def num_prefers(self, a1, a2):
        """The number of agents that prefer alternative `a1` over `a2`.

        """
        num = 0

        for voter in self.ballots.keys():
            if self.prefers(voter, a1, a2):
                num += 1

        return num
