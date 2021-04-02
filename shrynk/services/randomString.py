import string 
import random 

def generateRandomString():
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N)) 
    return res