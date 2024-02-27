import requests
import json
import os
from get_ids import *



url = "https://admin-api.axissecurity.com/api/v1.0/Users/"

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': os.environ['AXIS_API_KEY'],
  'Cookie': 'ax_session=1707811322.554.309.540450|59363e5f178f0b48e5dedc718c7f3b3e'
}

def add_user(group, user):
  uid = get_uid(user)
  payload = json.loads((requests.request("GET", url + uid, headers=headers, data={})).text)
  id = get_gid(group)
  group_id = {"id": id}
  payload["groups"].append(group_id)
  print(requests.request("PUT", url + uid, headers=headers, data=json.dumps(payload)))
  return requests.request("POST", url="https://admin-api.axissecurity.com/api/v1.0/Commit", headers=headers, data={})

def revoke_user(user):
  uid = get_uid(user)
  payload = json.loads((requests.request("GET", url + uid, headers=headers, data={})).text)
  payload["groups"].pop()
  return(requests.request("PUT", url + uid, headers=headers, data=json.dumps(payload)))

#print(update_user("remote_maintenance"))
#print(revoke_user("lukas_richter"))
