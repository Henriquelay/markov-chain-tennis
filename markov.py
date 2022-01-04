#!/bin/env python3

# Predicting the outcome of a game
# One can win with at least 3 points (4th will be set point) AND 1 or more points from the opponent
import random
# Returns 0 when P wins, 1 otherwise
def predict_game(P_chance: float):
    # P, Q
    points = [0,0]
    while True:
        if P_chance > random.random():
            points[0] += 1
            winner = 0
        else:
            points[1] += 1
            winner = 1
        if points[winner] > 3 and points[winner] - 1 > points[1-winner]:
            return winner

def predict_set(P_chance: float, tie_break=False):
    games_played = 0
    # P, Q
    points = [0, 0]
    while games_played < 6 and max(points) - 1 < min(points):
        games_played += 1
        if not tie_break and points[0] == 6 and points[1] == 6:
            return predict_set(P_chance, tie_break=True)
        points[predict_game(P_chance)] += 1
    return points.index(max(points))


# Return True if P has won the match, False otherwise
def predict_match(chances: [float, float]):
    # P, Q
    points = [0,0]
    for i in range(0,2):
        points[predict_game(chances[i])] += 1
    if points[0] == 1:
        points[predict_game(chances[2])] += 1
    return points[0] == 2


for _ in range(0,args.runs):
    print(predict_game(args.chance))
