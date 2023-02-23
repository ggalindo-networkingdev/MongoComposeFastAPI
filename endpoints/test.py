import pymongo
import urllib.parse
from fastapi import APIRouter, HTTPException, status, Query, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/test",  tags=["test"])
def test():
    try:
        username = urllib.parse.quote_plus('root')
        password = urllib.parse.quote_plus('rootpassword')
        myclient = pymongo.MongoClient(f"mongodb://{username}:{password}@172.25.0.2:27017")
        mydb = myclient["mydatabase"]
        mycol = mydb["customers"]
        mydict = { "name": "John", "address": "Highway 37" }
        x = mycol.insert_one(mydict)
        name = mydb.list_collection_names()
        final_name = f'{name} hello'
        print(mydb.list_collection_names())
        return JSONResponse({'device_list': final_name, 'msg': 'Found'})
    except Exception as e:
        print("========")
        print(e)
        final_name = f'{e}'
        return JSONResponse({'device_list': final_name, 'msg': 'Not Found'})

@router.get("/test2",  tags=["test"])
def test2():
    return JSONResponse({'hello': "Hello World"})
