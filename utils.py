import uuid
from datetime import datetime

def uid_hash()->str:
    return uuid.uuid4().hex  # 32-character hexadecimal string

def get_datetime()->str:
    return str(datetime.today())

    
    