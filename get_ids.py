import requests
import json
import os


url_u = "https://admin-api.axissecurity.com/api/v1.0/Users?pageNumber=1&pageSize=150"
url_g = "https://admin-api.axissecurity.com/api/v1.0/Groups?pageNumber=1&pageSize=150"

payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': os.environ['AXIS_API_KEY'],
  'Cookie': 'ax_session=1707811322.554.309.540450|59363e5f178f0b48e5dedc718c7f3b3e'
}

def get_uid(username):
    data = json.loads(requests.request("GET", url_u, headers=headers, data=payload).text)
    for i in data["data"]:
        if i["userName"] == username:
            return(i["id"])

def get_gid(name):
    data = json.loads(requests.request("GET", url_g, headers=headers, data=payload).text)
    for i in data["data"]:
        if i["name"] == name:
            return(i["id"])

def check_u(name):
    data = json.loads(requests.request("GET", url_u, headers=headers, data=payload).text)
    for i in data["data"]:
        if i["userName"] == name:
            return True
    return False
        

#print(get_uid("lukas_richter"))
#print(get_gid("remote_maintenance"))
