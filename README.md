# CSV Cleaner

A command-line tool for cleaning CSV files built with pure Python.

## Architecture
- `DataParser` — loads, validates, reports and analyses data (read-only)
- `DataCleaner` — inherits from DataParser, adds cleaning and saving (write operations)

## Features
- Handles missing values via mean, median, mode or drop
- Removes duplicate rows
- Validates file paths and handles errors gracefully
- Show data stats
- Cleans data
- Shows pre and post clean report
- Logs execution time for each operation

## How to Run
```bash
python3 csv_cleaner.py --input data.csv --output cleaned.csv --fill-method median --drop-duplicates
```

## Flags
| Flag | Options | Default | Description |
|------|---------|---------|-------------|
| --input | path | required | Input CSV path |
| --output | path | required | Output CSV path |
| --fill-method | mean/median/mode/drop | median | How to handle missing values |
| --drop-duplicates | flag | False | Remove duplicate rows |
| --stats | flag | False | Show data statistics |
