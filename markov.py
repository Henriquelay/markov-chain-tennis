#!/bin/env python3

import argparse
parser = argparse.ArgumentParser(description="Try to predict player's chance to win on a tennis match versus a known opponent")

default_runs_amount = 50

parser.add_argument("chances", metavar="P", type=float, nargs=2, help="player's chance to score against adversary")
parser.add_argument("-r", "--runs", metavar="RUNS", type=int, nargs="?", default=default_runs_amount, help="number of time to simulate a match. Higher numbers means more precision but more time calculating")
args = parser.parse_args()

# Predicting the outcome of a game
# One can win with at least 3 points (4th will be set point) AND 1 or more points from the opponent
import random
# Returns 0 when P wins, 1 otherwise
def predict_game(P_chance: float):
    # P, Q
    points = [0,0]
    winner = 0
    while not winner and points[winner] <= 3 and max(points) - 2 < min(points):
        draw = random.random()
        # print(f"Chance: {P_chance}, randomed: {draw}, result {P_chance > draw}")
        if P_chance > draw:
            winner = 0
        else:
            winner = 1
        points[winner] += 1
    return winner

def predict_set(P_chance: float, tie_break=False):
    # P, Q
    points = [0, 0]
    games_played = 0
    while games_played < 6 and max(points) - 2 < min(points):
        if not tie_break and points[0] == 6 and points[1] == 6:
            return predict_set(P_chance, tie_break=True)
        winner = predict_game(P_chance)
        games_played += 1
        points[winner] += 1
    return winner


# Return True if P has won the match, False otherwise
def predict_match(chances: list[float]):
    # P, Q
    points = [0,0]
    for i in range(0,2):
        points[predict_set(chances[i])] += 1
    if points[0] == 1:
        points[predict_set(chances[1])] += 1
    return bool(points[0] == 2)


for _ in range(0,args.runs):
    print(predict_match(args.chances))
