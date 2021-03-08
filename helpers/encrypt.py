import hashlib
import base64
import re

def sha256_base64(text):
    return base64.b64encode(hashlib.sha256(text.encode()).digest())

def check_if_sha256(text):
    pattern = r"^[A-Fa-f0-9]{64}$"
    if re.search(pattern,text):
        return True
    else:
        return False
