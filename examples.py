import csv
import random
from profile import Profile
from game import Game
from gametype import GameType
from analysis import Analysis

def main():

    print("\n### Loading data from .csv and running two types of games ###\n")

    csv_example = Profile.from_csv("examples/testprofile.csv")

    csv_example.print()

    csv_game_amendment = Game(GameType.AMENDMENT, ['c', 'b', 'a'], 2, csv_example)
    csv_game_successive = Game(GameType.SUCCESSIVE, ['c', 'b', 'a'], 2, csv_example)

    print(f"Outcome with amendment: {csv_game_amendment.outcome()}; with successive: {csv_game_successive.outcome()}")

    print("\n### Loading data from .txt and printing information ###\n")

    ex_5_2 = Profile.from_txt("examples/ex_5_2.txt")

    print("Example 5.2, Barberà and Gerber:\n")

    ex_5_2.print()

    ex_5_2.print_dominance()

    print("\n### Running multiple games with different quota ###\n")

    for q in [i + 1 for i in range(5)]:
        analysis = Analysis(GameType.AMENDMENT, ex_5_2, q)
        outcomes = analysis.quota_outcomes()
        print(f"q = {q}: {outcomes}")

    print("\n### Working with PrefLib .soc files ###\n")

    soc1 = Profile.from_soc("examples/ED-00004-00000008.soc")

    soc1.print()

    soc1.print_dominance()

    soc1_agenda = random.sample(list(soc1.alternatives), len(soc1.alternatives))

    soc1_game = Game(GameType.AMENDMENT, soc1_agenda, 2, soc1)

    print("Outcome of a .soc amendment game:", soc1_game.outcome())
    print("Agenda was", soc1_agenda)


if __name__ == "__main__":
    main()
