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

def detect_encoding(filename):
    result = subprocess.run(["file","-i",filename], capture_output=True, text=True)
    return result.stdout.split("charset")[-1].replace("\n","")[1:]


def get_emails_and_pwds(lines, filename):
    logging.info("Number of lines {}".format(len(lines)))
    emails = []
    passwords = []
    for idx,line in enumerate(lines):
        if idx % 35000 == 0 and idx > 0:
            write_to_txt(emails,passwords,filename)
            #logging.info("Emails {} : Passwords {}".format(len(emails),len(passwords)))
            emails = []
            passwords =[]
        try:
            data = re.findall(PATTERN,line)
            if data:
                email = data[0]
                password = line.replace(email,"")[1:]
                emails.append(email)
                passwords.append(password)
            else:
                data = re.split('[:;*]',line)
                if len(data) > 2:
                    line += " ---> INVALID LINE"
                elif len(data) == 2:
                    password = data[1]
                    passwords.append(password)
                    line += " ---> INVALID EMAIL"
                
                add_unprocessed_line(line)


        except Exception as e:
            logging.error("Error", exc_info=True)
    logging.info("Inserting last batch")
    logging.info("Emails {} : Passwords {}".format(len(emails),len(passwords)))
    write_to_txt(emails,passwords,filename)
    logging.info("Done")



def write_to_csv(emails, passwords,filename):

    with open(f"results/EMAILS-{filename.strip().reaplce(' ','-')}.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(emails)

    with open(f"results/PASSWORDS-{filename.strip().reaplce(' ','-')}.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(passwords)


def write_to_txt(emails,passwords,filename):
    with open(f"results/emails-{filename.strip().replace(' ','-')}.txt", "a") as f:
        f.write("\n".join(emails)+ "\n")

    with open(f"results/passwords-{filename.strip().replace(' ' ,'-')}.txt", "a") as f:
        f.write("\n".join(passwords)+ "\n")


def get_lines_from_file(filename):
    encoding = ["utf-8","latin_1"]
    for enc in encoding:
        try:
            with open(filename, encoding=enc) as f:
                logging.info("Collecting lines")
                lines = [line.replace("\n","").strip() for line in f.readlines() if line != ""]
                logging.info("Done")
                return lines
        except:
            continue

    return []

if __name__ == "__main__":

    COLLECTION_PATH = os.path.abspath(sys.argv[1])

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename="log.log"
    )
    parsed_files = get_parsed_files()
    for file in os.listdir(COLLECTION_PATH):
        filename = os.path.join(COLLECTION_PATH, file)
        if os.path.isdir(filename):
            for inner_file in os.listdir(filename):
                inner_filename = os.path.join(filename,inner_file)
                if inner_filename in parsed_files:
                    continue
                try:
                    logging.info("Processing {}".format(inner_filename))
                    lines = get_lines_from_file(inner_filename)
                    if lines:
                        get_emails_and_pwds(lines,file)
                        add_processed_file(inner_filename)
                    else:
                        logging.info("Didn't process {}".format(inner_filename))
                        add_unprocessed_file(inner_filename)
                        continue
                except Exception as e:
                    logging.error("Error at {}".format(inner_filename), exc_info=True)
                    add_unprocessed_file(inner_filename)
                    continue
       
    logging.info(f"Done parsing collection!")
