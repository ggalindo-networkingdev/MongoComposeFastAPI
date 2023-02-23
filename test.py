import pymongo
import urllib.parse
import time

username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('rootpassword')

myclient = pymongo.MongoClient(f"mongodb://{username}:{password}@0.0.0.0:27017")
mydb = myclient["mydatabase"]

time.sleep(2)

print(mydb.list_collection_names())