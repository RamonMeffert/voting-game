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

####
# To do:
# - check (for 1 large profile) influence of quota value on manipulability for both amendment and successive
# - run both procedures for Borda/Plurality and Amendment/Successive w/ 9 alternatives
##


def main(args):

    profiles = read_profiles(args.input_directory, args.n_alternatives)

    if len(profiles) > 0:
        print(f"Found {len(profiles)} profiles with {args.n_alternatives} alternatives")
    else:
        print(f"No profiles with {args.n_alternatives} alternatives found. Exiting.")
        exit()

    results = {}

    for filename, profile in profiles.items():
        winner = profile.winner(args.rule)
        n = len(profile.alternatives)
        quota = n / 2

        analysis = Analysis(args.procedure, profile, quota, winner)

        percentage, _ = analysis.outcomes()

        results[filename] = percentage

    if len(results) > 0:
        avg = sum(results.values()) / len(results)
    else:
        avg = 0

    print(f"This run produced the expected outcome {round(avg, 2)}% of the time.")

    os.makedirs(args.output_directory, exist_ok=True)

    output_filename = os.path.join(
        args.output_directory,
        f"{str(args.rule)}-{str(args.procedure)}-{args.n_alternatives}.log",
    )

    with open(output_filename, "w") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["average", avg])
        writer.writerow([])
        for filename, percentage in results.items():
            writer.writerow([filename, percentage])


def read_profiles(dir, alternatives):
    profiles = {}

    for file in os.scandir(dir):
        if file.path.endswith(".soc"):
            in_range = False

            with open(file) as cur_file:
                num_alternatives = int(cur_file.readline())
                if num_alternatives == alternatives:
                    in_range = True

            if in_range:
                profile = Profile.from_soc(file.path)
                profiles[Path(file.name).stem] = profile

    return profiles


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-m", "--n_alternatives", type=int, help="The number of alternatives", default=3
    )
    parser.add_argument(
        "-p",
        "--procedure",
        type=GameType.argparse,
        default="successive",
        choices=list(GameType),
        help="Which procedure to use",
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
        "-o",
        "--output_directory",
        type=str,
        default="./logs/",
        help="The directory to save output files to. Will be created if it doesn't exist already",
    )

    args = parser.parse_args()

    main(args)
