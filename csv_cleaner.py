import argparse
import csv
import sys
from pathlib import Path

class DataCleaner:
    
    def __init__(self, args: argparse.Namespace) -> None:
        self.input = args.input
        self.output = args.output
        self.fill_method = args.fill_method
        self.drop_duplicates = args.drop_duplicates
        self.count = 0
        self.data = []



def main() -> None:
    args = user_input()
    cleaner = DataCleaner(args)


def user_input() -> argparse.Namespace:
    parser =argparse.ArgumentParser()
    parser.add_argument("--input", help="add your dataset", required=True)
    parser.add_argument("--output", help="add your output path", required=True)
    parser.add_argument("--fill-method", help="add what to fill in blanks", choices=["mean", "median", "mode", "drop"], default="median")
    parser.add_argument("--drop-duplicates", help="add if true", action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()