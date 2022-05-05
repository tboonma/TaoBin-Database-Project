from connection import *

db = ConnectDatabase()
col = db.get_collection("customer")

for x in col.find({}):
    print(x)