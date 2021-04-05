import csv
import profile
import random
from ballot import Ballot
from typing import Set
from os import stat


class Profile:
    def __init__(self, ballots = {}, alternatives = set(), alternatives_names = None):
        # A ballot is a key-value pair where the key is the voter id and the
        # value is an ordered list of alternatives
        self.ballots = ballots

        # Save the available alternatives as a set
        self.alternatives = alternatives

        # Optionally save names of alternatives
        self.alternatives_names = alternatives_names


    @classmethod
    def from_csv(cls, path: str) -> 'Profile':
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
        ballots = {}
        alternatives = set()

        with open(path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",",
                             skipinitialspace = True, quoting = csv.QUOTE_MINIMAL)

            for voter in reader.fieldnames:
                voter_id = int(voter)
                # note: the Ballot constructor has a default value of [] for
                # its preference field, but not initialising it breaks the
                # program; all ballots then reference the same list. (???)
                ballots[voter_id] = Ballot(id=voter_id,preference=[])

            for line in reader:
                print(line)
                for voter in reader.fieldnames:
                    ballots[int(voter)].preference.append(line[voter])

        new_profile = cls(ballots, alternatives)

        # This will raise an error if the profile is invalid
        new_profile.__validate()

        return new_profile


    @classmethod
    def from_txt(cls, path: str) -> 'Profile':
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

        ballots = {}
        alternatives = set()

        with open(path) as txtfile:
            reader = txtfile.readlines()

            # save set of alternatives
            alternatives.update(reader[0].split(":")[1].split())

            # save voter preferences
            for voter in reader:
                split = voter.split(":", 1)
                voter_id = int(split[0])
                preference = split[1].split()
                ballots[voter_id] = Ballot(id=voter_id, preference=preference)

        # use constructor to create a profile
        new_profile = cls(ballots, alternatives)
        # This will raise an error if the profile is invalid
        new_profile.__validate()

        return new_profile


    @classmethod
    def from_soc(cls, path: str) -> 'Profile':
        """Imports a `.soc` file from PrefLib representing a complete strict order
        """

        ballots = {}
        alternatives = set()
        alternative_names = {}

        with open(path) as socfile:
            reader = socfile.readlines()

            cur_line = 0

            # read alternatives
            num_alternatives = int(reader[cur_line])
            cur_line += 1

            for alternative in range(cur_line, cur_line + num_alternatives):
                alternative_line = reader[alternative].split(",")
                alternative_id = alternative_line[0].strip()
                alternative_name = alternative_line[1].strip()

                alternatives.add(alternative_id)
                alternative_names[alternative_id] = alternative_name
                cur_line += 1

            # read info
            info = reader[cur_line].split(",")
            total_votes = int(info[0])
            unknown_1 = int(info[1])
            num_unique_ballots = int(info[2])
            cur_line += 1

            # read profile
            for ballot in range(cur_line, cur_line + num_unique_ballots):
                ballot_line = reader[ballot].split(",", maxsplit=1)
                ballot_id = ballot - cur_line + 1
                ballot_weight = int(ballot_line[0])
                ballot_preference = ballot_line[1].strip().split(",")
                ballot = Ballot(id=ballot_id, preference=ballot_preference, weight=ballot_weight)
                ballots[ballot_id] = ballot

        new_profile = cls(ballots, alternatives, alternative_names)
        new_profile.__validate()

        return new_profile


    @classmethod
    def random(cls, num_voters: int, num_alternatives: int) -> 'Profile':
        """Generate a random profile with the given number of voters and alternatives
        """

        alternatives = [ chr(c) for c in range(ord('a'), ord('a') + num_alternatives) ]
        ballots = {}

        for voter in [v + 1 for v in range(num_voters)]:
            ballots[voter] = random.sample(alternatives, num_alternatives)
        
        random_profile = cls(ballots, alternatives)
        random_profile.__validate()

        return random_profile


    def __validate(self):
        """Validates the profile by:

        * Checking the length of all ballots is the same
        * Checking if the set of alternatives is the same for all ballots
        """

        # Retrieve the first ballot and take the alternatives in there as the
        # available alternatives
        first_voter_id = next(iter(self.ballots))

        # update(list) on a Set adds all items in that list to the set
        self.alternatives.update(self.ballots.get(first_voter_id).preference)

        # iterate over voter preferences
        # (self.ballots.values() is a list of lists of alternatives)
        for voter, ballot in self.ballots.items():
            # if a ballot has a different number of alternatives than are
            # available, or if it contains alternatives not in the set of
            # alternatives, throw an error
            length_different = len(ballot.preference) != len(self.alternatives)
            alternatives_differ = set(ballot.preference).difference(self.alternatives)

            # Provide helpful error message
            if len(alternatives_differ) != 0:
                if length_different:
                    # Different length _and_ different composition
                    raise ValueError(f"\n\tVoter {voter} has a different set "
                                     "of alternatives than I was expecting. I was expecting "
                                     f"{len(self.alternatives)} alternatives but got "
                                     f"{len(ballot.preference)} instead.\n\tAlso, these alternatives "
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
                                 f"{len(ballot.preference)} instead.")


    def __sorted_alternatives(self):
        return sorted(list(self.alternatives))


    def ballot(self, id):
        """Returns the ballot of a voter with id `id`.

        Returns:
            [type]: [description]
        """
        return self.ballots[id]


    def prefers(self, id, a1, a2) -> bool:
        """Whether a voter with id `id` prefers alternative `a1` over `a2`.
        """

        ballot = self.ballot(id)

        # lower index means higher ranking
        return ballot.preference.index(a1) < ballot.preference.index(a2)


    def num_prefers(self, a1, a2):
        """The number of agents that prefer alternative `a1` over `a2`.

        """
        num = 0

        for voter in self.ballots.keys():
            if self.prefers(voter, a1, a2):
                num += 1

        return num


    def dominance(self):
        """Calculate the dominance matrix of a profile

        Returns:
            An 𝑚×𝑚 matrix representing the dominance relation P
        """
        sorted_alternatives = self.__sorted_alternatives()

        dominance = [[self.num_prefers(y, x) for x in sorted_alternatives] for y in sorted_alternatives]

        return dominance


    #TODO: Fix this to include weight
    def print_dominance(self):
        """Pretty-print a dominance matrix
        """

        dominance = self.dominance()

        # Print header
        print("Dominance matrix:\n")
        print("\t  │ ", end='')
        for x in self.__sorted_alternatives():
            print(x + " ", end='')
        print() # newline

        # Print separating line
        print("\t──┼", end='')
        for _ in range(len(self.alternatives)):
            print("──", end='')
        print()

        # Print rows
        for i, x in enumerate(self.__sorted_alternatives()):
            print(f"\t{x} │ ", end = '')
            for j, _ in enumerate(self.__sorted_alternatives()):
                print(str(dominance[i][j]) + " ", end='')
            print() # newline
        print() # newline

    
    def print(self):
        """Pretty-print a profile
        """

        maxlen = len(str(len(self.ballots)))
        for ballot in self.ballots.values():
            length = len(str(ballot.weight))
            if length > maxlen:
                maxlen = length

        print("Profile:\n")
        for voter, ballot in self.ballots.items():
            if ballot.weight == 1:
                print(f"\t{voter:{maxlen}} │ ", end='')
                for alternative in ballot.preference:
                    print(alternative, end=' ')
                print() # newline
            else:
                print(f"\t#{ballot.weight:{maxlen}} │ ", end='')
                for alternative in ballot.preference:
                    print(alternative, end=' ')
                print() # newline
        print() # newline

        if self.alternatives_names != None:
            print("IDs represent the following alternatives:\n")

            brk = 0
            for id, name in self.alternatives_names.items():
                brk += 1
                print(f"{id:>2}: {name:30}", end=' ')
                if brk % 3 == 0:
                    print()
            print()