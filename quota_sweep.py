import csv
import random
import os
import math
import argparse
from profile import Profile
from game import Game
from gametype import GameType
from analysis import Analysis
from rule import Rule
from enum import Enum
from pathlib import Path


def main(args):

    if args.n_alternatives > 10:
        print("This won't work")
        exit()

    profile = find_profile(args.input_directory, args.n_alternatives)

    if profile != None:
        filename, prof = profile
        print(f"Found a file with {args.n_alternatives} alternatives: {filename}")

        results = {}
        expected = prof.winner(args.rule)
        n_voters = len(prof.ballots)
        
        for q in [i + 1 for i in range(n_voters)]:
            analysis = Analysis(GameType.SUCCESSIVE, prof, q, expected)

            percentage, _ = analysis.outcomes()
            results[q] = percentage

        os.makedirs(args.output_directory, exist_ok=True)

        output_filename = os.path.join(
            args.output_directory,
            f"q-{str(args.rule)}-{args.n_alternatives}.log",
        )

        with open(output_filename, "w") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["file", filename])
            writer.writerow([])
            for quota, percentage in results.items():
                writer.writerow([quota, percentage])


def find_profile(dir, alternatives):
    """Tries to find a profile with a given number of alternatives
    """

    for file in os.scandir(dir):
        if file.path.endswith(".soc"):
            with open(file) as cur_file:
                num_alternatives = int(cur_file.readline())
                if num_alternatives == alternatives:
                    return Path(file.name).stem, Profile.from_soc(file.path)

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-r",
        "--rule",
        type=Rule.argparse,
        default="plurality",
        choices=list(Rule),
        help="Which rule to compare to. Note that only plurality and borda are implemented currently.",
    )
    parser.add_argument(
        "-i",
        "--input_directory",
        type=str,
        help="An input directory containing .soc files",
    )
    parser.add_argument(
        "-m",
        "--n_alternatives",
        type=int,
        help="The highest quota to analyse. This means this will try to find a profile with this number of alternatives.",
        default=3,
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        type=str,
        default="./logs/",
        help="The directory to save output files to. Will be created if it doesn't exist already",
    )

    args = parser.parse_args()

    main(args)