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


game_hist = list[list[int]]


def predict_game(
    P_chance: float, file: TextIO, game_state: list[list[int], list[int], int]
) -> tuple[game_hist, int]:
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


set_hist = tuple[tuple[list[int], list[game_hist]]]
def predict_set(
    P_chance: float,
    file: TextIO,
    game_state: list[list[int], list[int], int],
    tie_break=False,
) -> tuple[set_hist, int]:
    # P, Q
    points = [0, 0]
    game_count = 0
    lead_count = not tie_break
    hist = []
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
        hist.append((points.copy(), game_hist.copy()))
        points[
            winner
        ] += 1  # TODO Overflow happens, so games aren't unlimited like real games
        # print(f"Set winner: {['P', 'Q'][winner]}. Score: {points}")
    hist.append((points.copy(), [game_hist[-1]]))
    return (hist, winner)


match_hist = tuple[tuple[list[int], list[set_hist]]]
# Return True if P has won the match, False otherwise
def predict_match(P_chance: float, file: TextIO, run: int) -> tuple[match_hist, bool]:
    # P, Q
    points = [0, 0]
    hist = []
    hist.append((points.copy(), []))
    for i in range(0, 2):
        (set_hist, winner) = predict_set(P_chance, file, [[], points, [run]])
        hist.append((points.copy(), set_hist.copy()))
        points[winner] += 1
        # print(f"Match winner: {['P', 'Q'][winner]}")
    if points[0] == 1:
        # print("Tied matches. Playing roundoff")
        (set_hist, winner) = predict_set(P_chance, file, [[], points, [run]])
        hist.append((points.copy(), set_hist.copy()))
        points[winner] += 1
        # print(f"Match winner: {['P', 'Q'][winner]}")
    # print(f"last set: {typ(set_hist)}")
    hist.append((points.copy(), [set_hist[-1]]))
    return (hist, points[0] == 2)


if args.runs < 30:
    print("Can't use less than 30 runs. Setting runs to 30.")
    args.runs = 30


def typ(something, depth=0):
    if depth > 63:
        return "..."
    if type(something) == tuple:
        return "(" + ", ".join(typ(ding, depth + 1) for ding in something) + ")"
    elif type(something) == list:
        return "[" + (typ(something[0], depth + 1) if something else "(empty)") + "]"
    else:
        return str(type(something))


file = args.out
# file.write(
#     f"points_P,points_Q,games_P,games_Q,sets_P,sets_Q,run,P_chance\n"
# )
# for chance in args.chances:
#     for run in range(1, args.runs + 1):
#         (hist, winner) = predict_match(chance, file, run)
#         if winner:
#             winner = "P"
#         else:
#             winner = "Q"
#         # print(f"{(hist, winner)}")
#         last_print = {}
#         last_print.clear()
#         last_print.setdefault("game_pointsP", -1)
#         last_print.setdefault("game_pointsQ", -1)
#         last_print.setdefault("set_pointsP", -1)
#         last_print.setdefault("set_pointsQ", -1)
#         last_print.setdefault("match_pointsP", -1)
#         last_print.setdefault("match_pointsQ", -1)
#         for (match_points, set_hist) in hist:
#             for (set_points, game_hist) in set_hist:
#                 for game_points in game_hist:
#                     if game_points[0] == last_print["game_pointsP"]:
#                         game_points[0] = ""
#                     if game_points[1] == last_print["game_pointsQ"]:
#                         game_points[1] = ""
#                     if set_points[0] == last_print["set_pointsP"]:
#                         set_points[0] = ""
#                     if set_points[1] == last_print["set_pointsQ"]:
#                         set_points[1] = ""
#                     if match_points[0] == last_print["match_pointsP"]:
#                         match_points[0] = ""
#                     if match_points[1] == last_print["match_pointsQ"]:
#                         match_points[1] = ""
#                     fstring = f"{game_points[0]},{game_points[1]},{set_points[0]},{set_points[1]},{match_points[0]},{match_points[1]},{run},{chance}\n"
#                     # print(fstring, end="")
#                     last_print["match_pointsP"] = match_points[0]
#                     last_print["match_pointsQ"] = match_points[1]
#                     last_print["set_pointsP"] = set_points[0]
#                     last_print["set_pointsQ"] = set_points[1]
#                     last_print["game_pointsP"] = game_points[0]
#                     last_print["game_pointsQ"] = game_points[1]
#                     file.write(fstring)



# match_hist = tuple[tuple[list[int], list[set_hist]]]
# set_hist = tuple[tuple[list[int], list[game_hist]]]
# game_hist = list[list[int]]
file.write(
    f"tot_pts_P,tot_pts_Q,tot_games_P,tot_games_Q,tot_sets_P,tot_sets_Q,tot_run,tot_P_chance\n"
)
for chance in args.chances:
    for run in range(1, args.runs + 1):
        (match, winner) = predict_match(chance, file, run)
        match_points = match[-1][0]
        # print(match_points)
        set_points = [0, 0]
        for set in match:
            if set[1]:
                set_points[0] += set[1][-1][0][0]
                set_points[1] += set[1][-1][0][1]
                game_points = [0, 0]
                for game in set[1]:
                    game_points[0] += game[1][-1][0]
                    game_points[1] += game[1][-1][1]
        fstring = f"{set_points[0]},{set_points[1]},{match_points[0]},{match_points[1]},{run},{chance}\n"
        # print(fstring, end="")
        file.write(fstring)
