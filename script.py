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

RESULTS_PATH = "/home/ubuntu/mongo-import/results"
def get_emails_and_pwds(lines, filename, dir_name):
    root = os.path.join(RESULTS_PATH, dir_name)
    
    email_dir = os.path.join(root, "emails")
    password_dir = os.path.join(root, "passwords")
    unprocessed_dir = os.path.join(root, "unprocessed")
    
    email_filename = os.path.join(email_dir, f"EMAILS-{filename}")
    password_filename = os.path.join(password_dir, f"PASSWORDS-{filename}")
    unprocessed_filename = os.path.join(unprocessed_dir, f"UNPROCESSED-{filename}")
    
    if not os.path.exists(root):
        os.mkdir(root)
        os.mkdir(email_dir)
        os.mkdir(password_dir)
        os.mkdir(unprocessed_dir)

    logging.info("Number of lines {}".format(len(lines)))
    emails = []
    passwords = []
    unprocessed = []
    for idx,line in enumerate(lines):
        #if line.startswith("\n"):
        #    line = line[1:]
        if line.endswith("\n"):
            line = line[:-1]
        if line == "":
            continue
        if idx % 35000 == 0 and idx > 0:
            write_to_txt(emails,passwords,email_filename, password_filename)
            #logging.info("Emails {} : Passwords {}".format(len(emails),len(passwords)))
            emails = []
            passwords =[]
            if unprocessed:
                add_unprocessed_lines(unprocessed,unprocessed_filename)
            unprocessed = []
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
                
                unprocessed.append(line)


        except Exception as e:
            logging.error("Error", exc_info=True)
    logging.info("Inserting last batch")
    logging.info("Emails {} : Passwords {}".format(len(emails),len(passwords)))
    if unprocessed:
        add_unprocessed_lines(unprocessed,unprocessed_filename)
    write_to_txt(emails,passwords,email_filename, password_filename)
    logging.info("Done")

def write_to_txt(emails,passwords,email_filename, pwd_filename):
    if emails:
        with open(email_filename, "a") as f:
            f.write("\n".join(emails)+ "\n")
    if passwords:
        with open(pwd_filename, "a") as f:
            f.write("\n".join(passwords)+ "\n")


def get_lines_from_file(filename,inner_file,file_):
    encoding = ["utf-8","latin_1"]
    lines = []
    count = 0
    for enc in encoding:
        try:
            with open(filename, encoding=enc) as f:
                logging.info("Collecting lines")
                #lines = [line.replace("\n","").replace("\u","").strip() for line in f if line != "" and line.replace("\n","").replace("\u","").strip() != ""]
                lines = [line.strip() for line in f if line != "" and line != "\n"] 
                #for line in f:
                #    if line != "":
                #        temp = line
                #        if line.endswith("\n"):
                #            temp = line[:-1]
                #        if line.startswith("\n"):
                #            temp = temp[1:]
                #    if temp != "":
                #        count+=1
                #        lines.append(temp)
                
                    
                logging.info("Done")
                break
                #return lines
        except:
            lines = []
            continue
    if lines:
        get_emails_and_pwds(lines,inner_file,file_)
        add_processed_file(filename)
    else:
        logging.info("Didn't process {}".format(filename))
        add_unprocessed_file(filename)

    #return []

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
                    get_lines_from_file(inner_filename,inner_file,file)
                    #get_emails_and_pwds(lines,inner_file,file)
                except Exception as e:
                    logging.error("Error at {}".format(inner_filename), exc_info=True)
                    add_unprocessed_file(inner_filename)
                    continue
       
    logging.info(f"Done parsing collection!")
