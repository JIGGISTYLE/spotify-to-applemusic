import random
import string

def Genrate_random_string(length):
    charachters = string.ascii_letters + string.digits
    return "".join(random.choices(charachters,k=length))
