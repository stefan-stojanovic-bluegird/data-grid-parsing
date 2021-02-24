import csv
import os

def add_unprocessed_line(line):
    with open(f"results/unprocessed_lines.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([line])

def add_unprocessed_file(line):
    with open("results/unprocessed_files.csv","a") as f:
        writer = csv.writer(f)
        writer.writerow([line])

def add_processed_file(line):
    with open("results/processed_files.csv","a") as f:
        writer = csv.writer(f)
        writer.writerow([line])

def add_processed_collection(line):
    with open("results/processed_collections.csv","a") as f:
        writer = csv.writer(f)
        writer.writerow([line])

def get_parsed_files():
    parsed_files = []
    
    if os.path.exists("results/unprocessed_files.csv"):
        with open('results/unprocessed_files.csv', 'r') as f:
            reader = csv.reader(f)
            parsed_files.extend(list(reader))
    
    if os.path.exists("results/processed_files.csv"):
        with open('results/processed_files.csv', 'r') as f:
            reader = csv.reader(f)
            parsed_files.extend(list(reader))

    if os.path.exists("results/processed_collections.csv"):
        with open('results/processed_collections.csv', 'r') as f:
            reader = csv.reader(f)
            parsed_files.extend(list(reader))
    print(parsed_files)
    return parsed_files
