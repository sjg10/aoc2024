#!/usr/bin/env python3
import importlib
import sys
import glob
from timeit import default_timer as timer
from pathlib import Path


def import_days():
    """
    Import all days in the days/ directory, and return the list of days in order
    """
    days = sorted(Path(x).stem for x in glob.glob("day*.py", root_dir="days"))
    for libname in days:
        globals()[libname] = importlib.import_module(f"days.{libname}")
    return days


def run_tests(days):
    """
    Run the tests for each day
    """
    for libname in days:
        day = globals()[libname]
        print(f"{libname} START")
        print("**********************")
        with open(f"res/{libname}.txt") as data:
            start = timer()
            part1, part2 = day.run(data)
            end = timer()
        print(f"Part1: {part1}")
        print(f"Part1: {part2}")

        print(f"Elapsed time {(end - start) * 1000:.2f}ms")
        print("**********************")
        print()


if __name__ == "__main__":
    days = import_days()
    # Run all days, or if provided only those specified as args
    if len(sys.argv) > 1:
        days = sys.argv[1:]
    run_tests(days)
