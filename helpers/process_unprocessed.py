import os
import sys
import re
import csv
import subprocess
import logging
import datetime
import time
from helpers.errors import *
from helpers.pattern import PATTERN

def get_emails(lines, filename, dir_name):
    logging.info("Number of lines {}".format(len(lines)))
    emails = []
    for idx,line in enumerate(lines):
        try:
            data = re.findall(PATTERN,line)
            if data:
                email = data[0]
                emails.append(email)
        except Exception as e:
            logging.error("Error", exc_info=True)
    logging.info(f"Emails {len(emails)}")
    write_to_txt(emails,os.path.join(dir_name, f"emails-{filename}"))
    logging.info("Done")

def write_to_txt(emails,email_filename):
    if emails:
        with open(email_filename, "a") as f:
            f.write("\n".join(emails)+ "\n")

def process_line(line):
    line = line.split(" ")
    line = line[0]
    if line.endswith("\n"):
        line = line[:-1]
    return line

def process_lines(filename,dir_name,file_):
    encoding = ["utf-8","latin_1"]
    lines = []
    count = 0
    for enc in encoding:
        try:
            with open(filename, encoding=enc) as f:
                logging.info("Collecting lines")
                lines = [process_line(line.strip()) for line in f if line != "" and line != "\n" and "INVALID EMAIL" in line]
                logging.info("Done")
                break
                #return lines
        except:
            logging.error("err",exc_info = True)
            lines = []
            continue
    if lines:
        get_emails(lines,file_,dir_name)
    else:
        logging.info("Didn't process {}".format(filename))


if __name__ == "__main__":

    COLLECTION_PATH = os.path.abspath(sys.argv[1])

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename="process.log")
    for idx,filename in enumerate(os.listdir(COLLECTION_PATH)):
        logging.info(f"{idx}. {filename}")
        process_lines(os.path.join(COLLECTION_PATH,filename),os.path.join(COLLECTION_PATH,"emails"),filename)
                            
