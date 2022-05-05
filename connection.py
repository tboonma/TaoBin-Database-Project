"""
Connect to database and retrieve cluster data
"""
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from decouple import config

def ConnectDatabase():
    CERT_LOCATION = config('CERT_LOCATION', default='its-no-secret')
    uri = "mongodb+srv://taobin-project.cfwoi.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                        tls=True,
                        tlsCertificateKeyFile=CERT_LOCATION,
                        server_api=ServerApi('1'),
                        connect=False)

    db = client['taobin']
    return db
