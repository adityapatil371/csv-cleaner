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

    def load(self) -> None:
        try:
            with open(self.input) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.data.append(row)
                    self.count += 1
        except FileNotFoundError:
            print("incorect path")
            sys.exit(1)
        except UnicodeDecodeError:
            print("incorect file type")
            sys.exit(1)
    
    def report(self) -> None:
        if not self.data:
            print("initialise load first")
            sys.exit(1)
        print("summary: ")
        print(f"column names are {self.data[0].keys()}")
        print(f"row count is {self.count}")
        print(f"file size is {Path(self.input).stat().st_size}")

    def save(self) -> None:
        if not self.data:
            print("initialise load first")
            sys.exit(1)
        with open(self.output, 'w') as file:
            writer = csv.DictWriter(file, fieldnames= self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)

def main() -> None:
    args = user_input()
    cleaner = DataCleaner(args)
    cleaner.load()
    cleaner.report()
    cleaner.save()

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