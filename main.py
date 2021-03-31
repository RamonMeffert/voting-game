import csv
from profile import Profile
from game import Game
from gametype import GameType
from analysis import Analysis

def main():

    ex_5_2 = Profile.from_txt("ex_5_2.txt")

    for q in [i + 1 for i in range(5)]:
        analysis = Analysis(GameType.AMENDMENT, ex_5_2, q)
        outcomes = analysis.quota_outcomes()
        print(f"q = {q}: {outcomes}")


if __name__ == "__main__":
    main()
