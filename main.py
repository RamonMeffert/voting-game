import csv
from profile import Profile
from game import Game, GameType

def main():

    prof = Profile.from_txt("testprofile.txt")

    game = Game( type = GameType.SUCCESSIVE
               , agenda = ['a', 'b', 'c']
               , quota = 1
               , profile = prof
               )

    print("outcome:", game.outcome())


if __name__ == "__main__":
    main()
