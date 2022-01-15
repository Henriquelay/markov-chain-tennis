#!/bin/env python3

from typing import TextIO
import csv
import random
import argparse
parser = argparse.ArgumentParser(
    description="Try to predict player's chance to win on a tennis match versus a known opponent")

default_runs_amount = 30

parser.add_argument("chances", metavar="P", type=float,
                    nargs=2, help="player's chance to score against adversary")
parser.add_argument("-r", "--runs", metavar="RUNS", type=int, nargs="?", default=default_runs_amount,
                    help="number of time to simulate a match. Higher numbers means more precision but more time calculating")
parser.add_argument("--out", "--output", "-o", metavar="OUT", type=argparse.FileType('w',
                    encoding='UTF-8'), default="out.csv", help="Output file to store the resulting dataset")
args = parser.parse_args()


# Predicting the outcome of a game
# One can win with at least 3 points (4th will be set point) AND 1 or more points from the opponent
# Returns 0 when P wins, 1 otherwise

def predict_game(P_chance: float, file: TextIO):
    # P, Q
    points = [0, 0]
    games_played = 0
    while max(points) <= 3 or max(points) - min(points) < 2:
        games_played += 1
        draw = random.random()
        if P_chance > draw:
            winner = 0
        else:
            winner = 1
        points[winner] += 1
        # print(f"Chance: {P_chance}, randomed: {draw}, result {P_chance > draw}, {points}")
    return winner


def predict_set(P_chance: float, file: TextIO, tie_break=False):
    # P, Q
    points = [0, 0]
    game_count = 0
    lead_count = not tie_break
    while (tie_break and max(points) < 7) or (lead_count and (max(points) < 6 or max(points) - min(points) < 2)) or (not lead_count and max(points) < 7):
        game_count += 1
        # Turn off set win by 2 points difference when 5 x 5
        if lead_count and points[0] == 5 and points[1] == 5:
            print("Turning off lead_count strategy.")
            lead_count = False
        # Enable tie breaker mode when 6 x 6
        if not tie_break and points[0] == 6 and points[1] == 6:
            print("Tie breaker!")
            return predict_set(P_chance, file, tie_break=True)
        winner = predict_game(P_chance, file)
        points[winner] += 1
        print(f"Set winner: {['P', 'Q'][winner]}. Score: {points}")
    return winner


# Return True if P has won the match, False otherwise
def predict_match(chances: list[float], file: TextIO):
    # P, Q
    points = [0, 0]
    for i in range(0, 2):
        winner = predict_set(chances[i], file)
        points[winner] += 1
        print(f"Match winner: {['P', 'Q'][winner]}")
    if points[0] == 1:
        points[predict_set(chances[1], file)] += 1
        print(f"Match winner: {['P', 'Q'][winner]}")
    return bool(points[0] == 2)


if args.runs < 30:
    print("Can't use less than 30 runs. Setting runs to 30.")
    args.runs = 30


writer = csv.writer(args.out, delimiter=",")
for _ in range(0, args.runs):
    print(predict_match(args.chances, writer))
