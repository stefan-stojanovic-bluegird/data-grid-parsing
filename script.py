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


def get_emails_and_pwds(lines, filename, dir_name):
    if not os.path.exists(f"/home/ubuntu/mongo-import/results/{dir_name}"):
        os.mkdir(os.path.join("/home/ubuntu/mongo-import/results",dir_name))
    path = f"/home/ubuntu/mongo-import/results/{dir_name}/DATA-GRID-{filename}"
    logging.info("Number of lines {}".format(len(lines)))
    emails = []
    passwords = []
    unprocessed = []
    for idx,line in enumerate(lines):
        if line.startswith("\n"):
            line = line[1:]
        if line.endswith("\n"):
            line = line[:-1]
        if line == "":
            continue
        if idx % 35000 == 0 and idx > 0:
            write_to_txt(emails,passwords,path)
            #logging.info("Emails {} : Passwords {}".format(len(emails),len(passwords)))
            emails = []
            passwords =[]
            if unprocessed:
                add_unprocessed_lines(unprocessed,f"/home/ubuntu/mongo-import/results/{dir_name}/unprocessed_lines.txt")
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
    write_to_txt(emails,passwords,path)
    logging.info("Done")



def write_to_csv(emails, passwords,filename):

    with open(f"results/EMAILS-{filename.strip().reaplce(' ','-')}.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(emails)

    with open(f"results/PASSWORDS-{filename.strip().reaplce(' ','-')}.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(passwords)


def write_to_txt(emails,passwords,path):
    with open(path.replace("DATA-GRID","EMAILS") , "a") as f:
        f.write("\n".join(emails)+ "\n")

    with open(path.replace("DATA-GRID","PASSWORDS"), "a") as f:
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
