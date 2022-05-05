# from connection import *

# db = ConnectDatabase()
# col = db["customers"]

# for x in col.find():
#   print(x)
from decouple import config
CERT_LOCATION = config('CERT_LOCATION', default='its-no-secret')
print(CERT_LOCATION)