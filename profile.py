import csv
import profile
import random
from rule import Rule
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
    def random(cls, num_voters: int, num_alternatives: int, num_groups: int = None) -> 'Profile':
        """Generate a random profile with the given number of voters and alternatives.
        If the num_groups parameter is given, that number of different preferences will be generated
        and assigned to equal groups.
        """

        ## TODO: Add voter groups groups

        if num_groups == None:
            num_groups = num_voters

        alternatives = set([ chr(c) for c in range(ord('a'), ord('a') + num_alternatives) ])
        ballots = {}
        group_ballots = {}

        for group in [g + 1 for g in range(num_groups)]:
            group_ballots[group] = random.sample(alternatives, num_alternatives)

        for voter in [v + 1 for v in range(num_voters)]:
            preference = group_ballots[(voter - 1) % num_groups + 1]
            ballots[voter] = Ballot(id=voter, preference=preference)

        random_profile = cls(ballots, alternatives)
        random_profile.__validate()

        return random_profile


    def alternative_name(self, name) -> str:
        """Helper method for printing the name of an alternative.
        """

        if self.alternatives_names != None:
            return self.alternatives_names[name]
        else:
            return name


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

        for ballot in self.ballots.values():
            if self.prefers(ballot.id, a1, a2):
                num += ballot.weight

        return num


    def dominance(self):
        """Calculate the dominance matrix of a profile

        Returns:
            An 𝑚×𝑚 matrix representing the dominance relation P
        """
        sorted_alternatives = self.__sorted_alternatives()

        dominance = [[self.num_prefers(y, x) for x in sorted_alternatives] for y in sorted_alternatives]

        return dominance


    def print(self):
        """Pretty-print a profile
        """

        maxlen = len(str(len(self.ballots)))
        for ballot in self.ballots.values():
            length = len(str(ballot.weight))
            if length > maxlen:
                maxlen = length

        has_weights = max([ballot.weight for ballot in self.ballots.values()]) > 1

        print("Profile:\n")
        for voter, ballot in self.ballots.items():
            if has_weights:
                print(f"\t#{ballot.weight:{maxlen}} │ ", end='')
                for alternative in ballot.preference:
                    print(alternative, end=' ')
                print() # newline
            else:
                print(f"\t{voter:{maxlen}} │ ", end='')
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


    def print_dominance(self):
        """Pretty-print a dominance matrix
        """

        dominance = self.dominance()

        maxlen = len(str(max(max(dominance))))
        for x in self.__sorted_alternatives():
            name = self.alternative_name(x)
            if len(name) > maxlen:
                maxlen = len(name)

        # Print header
        print("Dominance matrix:\n")
        print("\t", end='')
        for _ in range(maxlen):
            print(" ", end='')
        print(" │ ", end='')
        for x in self.__sorted_alternatives():
            name = self.alternative_name(x)
            print(f"{name:^{maxlen + 1}}", end='')
        print() # newline

        # Print separating line
        print("\t", end='')
        for _ in range(maxlen + 1):
            print("─", end='')
        print("┼", end='')
        for _ in range(len(self.alternatives) * (maxlen + 1)):
            print("─", end='')
        print()

        # Print rows
        for i, x in enumerate(self.__sorted_alternatives()):
            name = self.alternative_name(x)
            print(f"\t{name:{maxlen}} │ ", end = '')
            for j, _ in enumerate(self.__sorted_alternatives()):
                print(f"{str(dominance[i][j]):^{maxlen + 1}}", end='')
            print() # newline
        print() # newline


    def winner(self, rule: Rule):
        if rule == Rule.PLURALITY:
            return self.__winner_plurality()
        elif rule == Rule.BORDA:
            return self.__winner_borda()
        elif rule == Rule.CONDORCET:
            return self.__winner_condorcet()
        elif rule == Rule.WEAK_CONDORCET:
            return self.__winner_weak_condorcet()


    def __winner_plurality(self):
        """Plurality with alphabetic tie-breaking
        """

        # initialize dictionary of plurality scores for all alternatives with an
        # initial value of 0
        plur_score = dict.fromkeys(self.alternatives, 0)

        # Calculate plurality scores by traversing all ballots
        for ballot in self.ballots.values():
            # the top choice for the current ballot
            voter_max = ballot.preference[0]

            plur_score[voter_max] += ballot.weight

        (winner_id, winner_score) = plur_score.popitem()

        for alternative, score in plur_score.items():
            if score > winner_score:
                winner_id = alternative
                winner_score = score
            elif score == winner_score:
                # Tie breaking. Sort alphabetically and take first item.
                # Score is unchanged, so doesn't need to be updated
                winner_id = sorted([str(winner_id), str(alternative)])[0]

        return winner_id


    def __winner_borda(self):
        m = len(self.alternatives)
        borda_score = dict.fromkeys(self.alternatives, 0)

        for ballot in self.ballots.values():
            for index, alternative in enumerate(ballot.preference):
                # calculate weight
                w = m - index - 1
                # update borda score
                borda_score[alternative] += w

        outcome = max(borda_score, key = borda_score.get)

        return outcome
    

    def __winner_condorcet(self):
        raise NotImplementedError()


    def __winner_weak_condorcet(self):
        raise NotImplementedError()