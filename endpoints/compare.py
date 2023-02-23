import json
import requests
import openpyxl
import io
from pathlib import Path
from fastapi import APIRouter, HTTPException, status, Query, UploadFile
from fastapi.responses import JSONResponse

from netbox import get_devices_byModel


router = APIRouter()
master_url = "http://127.0.0.1:8000"
local_url= "http://0.0.0.0:8001"

@router.get("/get_all_devices_by_type",  tags=["compare"])
def get_all_devices_by_type(device_type_name:str = Query(..., description="return a devices list from Netbox (E.g., name = Cisco 1841) ")):
    try:
        device_type_list = json.loads(device_type_name.replace("'", '"'))
        device_list = get_devices_byModel(device_type_list)
        return JSONResponse({'device_list': device_list, 'msg': 'Found'})
    except:
        return JSONResponse({'device_list': [], 'msg': 'Not Found'})

@router.get('/extracting_from_mongo',  tags=["compare"])
async def parse_imported_file():
    url=f"{master_url}/experimental/upload"
    mongo_devices = []
    url=f"{master_url}/experimental/sts/view?page_number=1&total_doc_count=400"
    r = requests.get(url)
    api_response = r.json()
    for device in api_response['data']:
        mongo_devices.append(device)
    return JSONResponse({'device_list': mongo_devices, 'msg': 'Found'})

@router.get("/comparing_version_from_netbox",  tags=["compare"])
def comparing_version_from_netbox():
    r = requests.get(url=f'{local_url}/api/extracting_from_mongo')
    device_type_list=[]
    device_type_comparison=[]
    mongo_device_list = r.json()['device_list']
    for device in mongo_device_list:
        device_type=device['device_info']['device_type']
        need_version= device['sts_info']['approved_version']
        device_type_list.append(device_type)
        device_type_comparison.append({'device_type': device_type, 'need_version': need_version})
    r = requests.get(url=f'{local_url}/api/get_all_devices_by_type?device_type_name={device_type_list}')
    netbox_devices = r.json()['device_list']
    devices_report = []
    for comparison in device_type_comparison:
        for device in netbox_devices:
            if comparison['device_type'] == device['device_type']['model']:
                final_device ={}
                final_device['device_name']=device['name']
                final_device['device_model']=device['device_type']['model']
                final_device['running_code']=device['custom_fields']['os_version'] 
                final_device['current_approved_code']= comparison['need_version']
                if device['custom_fields']['os_version'] == comparison['need_version']:
                    final_device['upgrade']='Not Required'
                    final_device['compliant']=True
                else:
                    final_device['upgrade']='Upgrade'
                    final_device['compliant']=False
                devices_report.append(final_device)
    return JSONResponse({'devices_report': devices_report})
        

            

    

    

    
    