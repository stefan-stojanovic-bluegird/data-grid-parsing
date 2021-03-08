from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys
import urllib
import logging

load_dotenv()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename="import.log")

PASS = urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))
URI = f'mongodb://{os.environ.get("MONGO_USER")}:{PASS}@{os.environ.get("MONGO_HOST")}:27017/?authSource=credentials'
db=MongoClient(URI).credentials

def insert_emails(lines):
    results = []
    batch_size = 100000
    line_count = len(lines) // batch_size + 2 
    
    for i in range(1,line_count):
        logging.info(f"Inserting {i} batch of emails")
        begin = (i-1) * batch_size
        end = i * batch_size
        if lines[begin:end]:
            db.emails.insert_many([{ "email" : email.lower() } for email in lines[ begin:end ]])
    
    logging.info("Success!" )

def insert_passwords(lines):
    results = []
    batch_size = 100000
    line_count = len(lines) // batch_size + 2
    
    for i in range(1,line_count):
        logging.info(f"Inserting {i} batch of passwords")
        begin = (i-1) * batch_size
        end = i * batch_size
        if lines[begin:end]:
            db.passwords.insert_many([{"password" : password } for password in lines[begin:end]])

    logging.info("Success!")


        
def strip_last(line):
    if line.endswith("\n"):
        return line[:-1]
    else:
        return line

def process_lines(filename,group):
    encoding = ["utf-8","latin_1"]
    lines = []
    count = 0
    for enc in encoding:
        try:
            with open(filename, encoding=enc) as f:
                logging.info("Collecting lines")
                lines = [strip_last(line.strip()) for line in f if line != "" and line != "\n"]                     
                logging.info("Done")
                break
                #return lines
        except:
            lines = []
            logging.error("Err", exc_info=True)
            continue
    if lines:
        logging.info(f"Inserting {filename}")
        if "emails" in group:
            insert_emails(lines)
        else:
            insert_passwords(lines) 
    else:
        logging.info("Didn't process {}".format(filename))

RESULTS_PATH = sys.argv[1]
parsed_files = []
with open("newly-imported.txt") as f:
    parsed_files = [strip_last(line.split("Processing")[-1].strip()) for line in f if line != "" and line != "\n"]
for dir in os.listdir(RESULTS_PATH):
    dir_path = os.path.join(RESULTS_PATH,dir)
    if os.path.isdir(dir_path):
        for group in os.listdir(dir_path):
            group_path = os.path.join(dir_path,group)
            if "emails" in group or "passwords" in group :
                for group_file in os.listdir(group_path):
                    group_file_path = os.path.join(group_path,group_file)
                    if group_file_path in parsed_files:
                        logging.info(f"Allready parsed {group_file_path}")
                        continue
                    logging.info("Processing {}".format(group_file_path))
                    process_lines(group_file_path,group)     
            
            

                



        
        


