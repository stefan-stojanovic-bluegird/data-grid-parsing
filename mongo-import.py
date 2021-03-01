from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv
load_dotenv()
import urllib

PASS = urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))
URI = f'mongodb://{os.environ.get("MONGO_USER")}:{PASS}@{os.environ.get("MONGO_HOST")}:27017/?authSource=credentials'
db=MongoClient(URI).credentials

RESULTS_PATH = sys.argv[1]
for dir in os.listdir(RESULTS_PATH):
    dir_path = os.path.join(RESULTS_PATH,dir)
    if os.path.isdir(dir_path):
        for group in os.listdir(dir_path):
            group_path = os.path.join(dir_path,group)
            if "emails" in group:
                for email_file in os.listdir(group_path):

            

                



        
        


