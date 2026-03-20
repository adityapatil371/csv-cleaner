import argparse
import csv
import sys
from pathlib import Path
import time
from collections import Counter
import statistics

def log_execution(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print(f"took {end - start} seconds")
        return result
    return wrapper

class DataCleaner:
    
    def __init__(self, args: argparse.Namespace) -> None:
        self.input = args.input
        self.output = args.output
        self.fill_method = args.fill_method
        self.drop_duplicates = args.drop_duplicates
        self.stat = args.stats 
        self.count = 0
        self.data = []

    @log_execution
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

    @log_execution   
    def report(self) -> None:
        if not self.data:
            print("initialise load first")
            sys.exit(1)
        print("summary: ")
        print(f"column names are {self.data[0].keys()}")
        print(f"row count is {self.count}")
        print(f"file size is {Path(self.input).stat().st_size}")

    @log_execution
    def save(self) -> None:
        if not self.data:
            print("initialise load first")
            sys.exit(1)
        with open(self.output, 'w') as file:
            writer = csv.DictWriter(file, fieldnames= self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)

    @log_execution
    def stats(self) -> None:
        if self.stat:
            for col in self.data[0].keys():
                values = [row[col] for row in self.data]
                try:
                    num_values = [float(value) for value in values]
                    print(f"mean is {statistics.mean(num_values)}")
                    print(f" stdev is {statistics.stdev(num_values)}")
                except ValueError:
                    print(Counter(values))

                    

class DataValidator(DataCleaner):
    @log_execution
    def validate(self) -> None:
        for col in self.data[0].keys():
            if not col.isidentifier():
                print(f"warning {col} is not valid")
            if all([row[col] == '' for row in self.data]):
                print(f"warning {col} is empty")
                

def main() -> None:
    args = user_input()
    validator = DataValidator(args)
    validator.load()
    validator.validate()
    validator.report()
    validator.save()
    validator.stats()

def user_input() -> argparse.Namespace:
    parser =argparse.ArgumentParser()
    parser.add_argument("--input", help="add your dataset", required=True)
    parser.add_argument("--output", help="add your output path", required=True)
    parser.add_argument("--fill-method", help="add what to fill in blanks", choices=["mean", "median", "mode", "drop"], default="median")
    parser.add_argument("--drop-duplicates", help="add if true", action='store_true')
    parser.add_argument("--stats", help="add if stats analysis is needed", action='store_true')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()