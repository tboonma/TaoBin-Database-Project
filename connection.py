"""
Connect to database and retrieve cluster data
"""
from pymongo import MongoClient
from decouple import config


CERT_LOCATION = config('CERT_LOCATION', default='its-no-secret')


class ConnectDatabase:
    def __init__(self) -> None:
        uri = "mongodb+srv://taobin-project.cfwoi.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
        self.__client = MongoClient(uri,
                            tls=True,
                            tlsAllowInvalidCertificates=True,
                            tlsCertificateKeyFile=CERT_LOCATION,
                            connect=False)
        self.db = self.__client['taobin']

    def get_collection(self, collection_name):
        return self.db[collection_name]
