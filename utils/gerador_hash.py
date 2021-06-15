# coding: utf-8
from datetime import datetime
import hashlib
import random

def gerar_hash():
    return hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()