from connection import *

db = ConnectDatabase()
col = db["customers"]

for x in col.find({}):
    print(x)