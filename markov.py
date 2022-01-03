#!/bin/env python3
import argparse
parser = argparse.ArgumentParser(description="Try to predict player's chanceto win on a tennis match versus a known opponent")

default_runs_amount = 50

parser.add_argument("chance", metavar="P", type=float, nargs=1, help="player's chance to score against adversary")
parser.add_argument("-r", "--runs", metavar="RUNS", type=int, nargs="?", default=default_runs_amount, help="number of time to simulate a match. Higher numbers means more precision but more time calculating")
