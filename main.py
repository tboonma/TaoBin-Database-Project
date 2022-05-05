from connection import *

db = ConnectDatabase()
col = db["customers"]

print(col.count_documents({}))
