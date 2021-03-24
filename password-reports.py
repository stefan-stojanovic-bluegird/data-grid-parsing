from pymongo import MongoClient
from dotenv import load_dotenv
from helpers.encrypt import *
from prettytable import PrettyTable
import binascii
import os
import sys
import urllib
import logging
import re

load_dotenv()

PASS = urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))
URI = f'mongodb://{os.environ.get("MONGO_USER")}:{PASS}@{os.environ.get("MONGO_HOST")}:27017/?authSource=credentials'
db=MongoClient(URI).credentials

def with_delimiter(number):
    return f"{number:,}".replace(",",".")


def count(query):
    return with_delimiter(db.passwords.count_documents(query))

if __name__ == "__main__":
    
    prettytable = PrettyTable(["Type of Report", "Count"])
    results = {
            "123 used" : count({ "password" : "123"}),
            "1234 used" : count({ "password" : "1234"}),
            "12345 used" : count({ "password" : "12345"}),
            "123456 used" : count({ "password" : "123456"}),
            "1234567 used" : count({ "password" : "1234567"}),
            "12345678 used" :  count({ "password" : "12345678"}),
            "123456789 used" : count({ "password" : "123456789"}),
            "qwerty used" : count({"password" : re.compile("qwerty", re.IGNORECASE) })}


    for key,value in results.items():
        prettytable.add_row([key,value])

    print(prettytable)

    


    
            

                



        
        


