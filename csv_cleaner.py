import argparse
import csv
import sys
from pathlib import Path
import time
from collections import Counter
import statistics
import re

def log_execution(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print(f"took {end - start} seconds")
        return result
    return wrapper

class DataParser:
    
    def __init__(self, args: argparse.Namespace) -> None:
        self.input = args.input
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
    def validate(self) -> None:
        for col in self.data[0].keys():
            if not col.isidentifier():
                print(f"warning {col} is not valid")
            if all([row[col] == '' for row in self.data]):
                print(f"warning {col} is empty")

    @log_execution   
    def input_report(self) -> None:
        if not self.data:
            print("initialise load first")
            sys.exit(1)
        print("summary: ")
        print(f"column names are {self.data[0].keys()}")
        print(f"row count is {self.count}")
        print(f"file size is {Path(self.input).stat().st_size}")

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


class DataCleaner(DataParser):
    
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)
        self.output = args.output
        self.fill_method = args.fill_method
        self.drop_duplicates = args.drop_duplicates
        
    @log_execution
    def clean(self) -> None:
        self.colname = list(self.data[0].keys())
        self.rowcount = self.count
        self.filesize = Path(self.input).stat().st_size
        for col in list(self.data[0].keys()): 
            if not col.isidentifier():
                new_col = re.sub(r'[^\w]', '_', col)
                for row in self.data:
                    row[new_col] = row.pop(col)
        for col in list(self.data[0].keys()):
            if all([row[col] == '' for row in self.data]):
                for row in self.data:
                    del row[col] 
        if self.drop_duplicates:
            seen = set()
            unique = []
            for row in self.data:
                key = tuple(row.items())
                if key not in seen:
                    seen.add(key)
                    unique.append(row)
            self.data = unique
        if self.fill_method == "drop":
            self.data = [row for row in self.data if all(v != '' for v in row.values())]
        else:
            for col in list(self.data[0].keys()):
                values = [row[col] for row in self.data if row[col] != '']
                try:
                    numeric = [float(v) for v in values]
                    if self.fill_method == "mean":
                        fill_value = statistics.mean(numeric)
                    if self.fill_method == "mode":
                        fill_value = statistics.mode(numeric)
                    if self.fill_method == "median":
                        fill_value = statistics.median(numeric)
                    for row in self.data:
                        if row[col] == '':
                            row[col] = fill_value
                except ValueError:
                    print("non numeric cell will remain empty")
        print("columns after clean:", list(self.data[0].keys()))

    @log_execution
    def output_report(self):
        print(f"column names before clean are {self.colname}")
        print(f"row count before clean is {self.rowcount}")
        print(f"file size before clean is {self.filesize}")
        print(f"column names after clean are {self.data[0].keys()}")
        print(f"row count after clean is {self.count}")
        print(f"file size after clean is {Path(self.input).stat().st_size}")
    
    @log_execution
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
    cleaner.validate()
    cleaner.input_report()
    cleaner.stats()
    cleaner.clean()
    cleaner.output_report()
    cleaner.save()

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