import os
import sys
import re
import csv
import subprocess



def detect_encoding(filename):
    result = subprocess.run(["file",filename], capture_output=True, text=True)
    return result.stdout.split(filename)[1].split(" ")[1]

def get_emails_and_pwds(lines,filename):
    pattern = r"([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)"
    emails = []
    passwords = []
    for line in lines:
        email = re.findall(pattern,line)
        if email:
            email = email[0]
        else:
            email = line.split(":")
            if len(email) > 1:
                email = email[0]
                print(email)
            else:
                print(f"No email found : {line}\t {filename}")
                continue
        emails.append([email])
        password = line.replace(email,"")[1:]
        passwords.append([password])
    
    return emails,passwords

    

def write_to_csv(lines,filename):
    emails,passwords = get_emails_and_pwds(lines,filename)
    with open("results/emails.csv","a") as f:
        writer = csv.writer(f)
        writer.writerows(emails)
    
    with open("results/passwords.csv","a") as f:
        writer = csv.writer(f)
        writer.writerows(passwords)

if __name__ == "__main__":
    COLLECTION_PATH = os.path.abspath(sys.argv[1])
    pattern = r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
    for file in os.listdir(COLLECTION_PATH):
        filename = os.path.join(COLLECTION_PATH, file)
        if os.path.isdir(filename):
            for inner_file in os.listdir(filename):
                inner_filename = os.path.join(filename,inner_file)
                enc=detect_encoding(inner_filename)
                with open(inner_filename,"r",encoding=enc) as f:
                    lines = [line.strip() for line in f.readlines() if line != ""]
                    write_to_csv(lines,inner_filename)





