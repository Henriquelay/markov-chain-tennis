#!/bin/env python3

from typing import TextIO
import random
import argparse

parser = argparse.ArgumentParser(
    description="Try to predict player's chance to win on a tennis match versus a known opponent"
)

default_runs_amount = 30

parser.add_argument(
    "chances",
    metavar="P",
    type=float,
    nargs=2,
    help="player's chance to score against adversary",
)
parser.add_argument(
    "-r",
    "--runs",
    metavar="RUNS",
    type=int,
    nargs="?",
    default=default_runs_amount,
    help="number of time to simulate a match. Higher numbers means more precision but more time calculating",
)
parser.add_argument(
    "--out",
    "--output",
    "-o",
    metavar="OUT",
    type=argparse.FileType("w", encoding="UTF-8"),
    default="out.csv",
    help="Output file to store the resulting dataset",
)
args = parser.parse_args()

# Predicting the outcome of a game
# One can win with at least 3 points (4th will be set point) AND 1 or more points from the opponent
# Returns 0 when P wins, 1 otherwise


def predict_game(
    P_chance: float, file: TextIO, game_state: list[list[int], list[int], int]
):
    # P, Q
    points = [0, 0]
    games_played = 0
    hist = []
    while max(points) <= 3 or max(points) - min(points) < 2:
        games_played += 1
        draw = random.random()  # [0,1)
        if P_chance > draw:
            winner = 0
        else:
            winner = 1
        hist.append(points.copy())
        points[winner] += 1
        # print(f"Chance: {P_chance}, randomed: {draw}, result {P_chance > draw}, {points}")
    hist.append(points.copy())
    return (hist, winner)


def predict_set(
    P_chance: float,
    file: TextIO,
    game_state: list[list[int], list[int], int],
    tie_break=False,
):
    # P, Q
    points = [0, 0]
    game_count = 0
    lead_count = not tie_break
    hist = []
    hist.append((points.copy(), [[0,0]]))
    while (
        (tie_break and max(points) < 7)
        or (lead_count and (max(points) < 6 or max(points) - min(points) < 2))
        or (not lead_count and max(points) < 7)
    ):
        game_state[0] = points
        game_count += 1
        # Turn off set win by 2 points difference when 5 x 5
        if lead_count and points[0] == 5 and points[1] == 5:
            # print("Turning off lead_count strategy.")
            lead_count = False
        # Enable tie breaker mode when 6 x 6
        if not tie_break and points[0] == 6 and points[1] == 6:
            # print("Tie breaker!")
            return predict_set(P_chance, file, game_state, tie_break=True)
        (game_hist, winner) = predict_game(P_chance, file, game_state)
        points[
            winner
        ] += 1  # TODO Overflow happens, so games aren't unlimited like real games
        hist.append((points.copy(), game_hist.copy()))
        # print(f"Set winner: {['P', 'Q'][winner]}. Score: {points}")
    # hist.append((points.copy(), [game_hist[-1]]))
    return (hist, winner)


# Return True if P has won the match, False otherwise
def predict_match(chances: float, file: TextIO, run: int):
    # P, Q
    points = [0, 0]
    hist = []
    hist.append((points.copy(), []))
    for i in range(0, 2):
        (set_hist, winner) = predict_set(chances, file, [[], points, [run]])
        hist.append((points.copy(), set_hist.copy()))
        points[winner] += 1
        # print(f"Match winner: {['P', 'Q'][winner]}")
    if points[0] == 1:
        # print("Tied matches. Playing roundoff")
        (set_hist, winner) = predict_set(chances, file, [[], points, [run]])
        hist.append((points.copy(), set_hist.copy()))
        points[winner] += 1
        # print(f"Match winner: {['P', 'Q'][winner]}")
    # hist.append((points.copy(), set_hist.copy()))
    return (hist, points[0] == 2)


if args.runs < 30:
    print("Can't use less than 30 runs. Setting runs to 30.")
    args.runs = 30


file = args.out
file.write(f"Game;Set;Match;Run;P\n")
for chance in args.chances:
    for run in range(1, args.runs+1):
        (hist, winner) = predict_match(chance, file, run)
        if winner:
            winner = "P"
        else:
            winner = "Q"
        # print(f"{(hist, winner)}")
        for (match_points, set_hist) in hist:
            for (set_points, game_hist) in set_hist:
                for game_points in game_hist:
                    fstring = f"{game_points[0]}-{game_points[1]},{set_points[0]}-{set_points[1]},{match_points[0]}-{match_points[1]},{run},{chance}\n"
                    # print(fstring, end="")
                    file.write(fstring)
