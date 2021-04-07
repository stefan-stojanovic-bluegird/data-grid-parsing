from pymongo import MongoClient
from dotenv import load_dotenv
from helpers.encrypt import *
import binascii
import os
import sys
import urllib
import logging

load_dotenv()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename="fb.log")

PASS = urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))
URI = f'mongodb://{os.environ.get("MONGO_USER")}:{PASS}@{os.environ.get("MONGO_HOST")}:27017/?authSource=credentials'
db=MongoClient(URI).credentials

def insert_emails(lines):
    results = []
    
    logging.info(f"Inserting emails")
    db.emails.insert_many([{ "email" : email.lower() , "breach_source" : "facebook"} for email in lines])
    
    logging.info("Success!" )

def insert_passwords(lines):
    logging.info("Inserting passwords")
    results = []
    db.hashednew.insert_many([{"password" : password } for password in lines])
    logging.info("Success!")

def insert_phones(lines):
    results = []
    logging.info("Inserting phones")
    db.phones.insert_many([{"phone" : phone , "breach_source" : "facebook"} for phone in lines])
    logging.info("Success!")



        
def strip_last(line):
    if line.endswith("\n"):
        line = line[:-1]
    if check_if_sha256(line):
        return binascii.unhexlify(line)
    else:
        return sha256_base64(line)

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
#with open("newly-imported.txt") as f:
#    parsed_files = [strip_last(line.split("Processing")[-1].strip()) for line in f if line != "" and line != "\n"]
for dir in os.listdir(RESULTS_PATH):
    dir_path = os.path.join(RESULTS_PATH,dir)
    if os.path.isdir(dir_path):
        for country_file in os.listdir(dir_path):
            country_full_path = os.path.join(dir_path,country_file)
            if "splitted" in country_full_path:
                for splitted_file in os.listdir(country_full_path):
                    print(splitted_file)
             
            
            

                



        
        


