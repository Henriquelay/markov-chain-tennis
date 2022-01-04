#!/bin/env python3
import argparse
parser = argparse.ArgumentParser(description="Try to predict player's chanceto win on a tennis match versus a known opponent")

default_runs_amount = 50

parser.add_argument("chance", metavar="P", type=float, help="player's chance to score against adversary")
parser.add_argument("-r", "--runs", metavar="RUNS", type=int, nargs="?", default=default_runs_amount, help="number of time to simulate a match. Higher numbers means more precision but more time calculating")
args = parser.parse_args()

# Predicting the outcome of a set
# One can win with at least 3 points (4th will be set point) AND 1 or more points from the opponent
import random
# Returns True when P wins, False otherwise
def predict_set(P: float):
    # P, Q
    points = [0,0]
    while True:
        if P > random.random():
            points[0] += 1
            winner = 0
        else:
            points[1] += 1
            winner = 1
        if points[winner] > 3 and points[winner] - 1 > points[1-winner]:
            return not bool(winner)

for _ in range(0,args.runs):
    print(predict_set(args.chance))
