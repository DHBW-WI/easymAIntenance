import requests
import json
import streamlit as st
from get_ids import get_gid 

url = "https://admin-api.axissecurity.com/api/v1.0/Users"

headers = {                                         # Header mit den API_Informationen
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': st.secrets["AXIS_API_KEY"],
  'Cookie': 'ax_session=1707811322.554.309.540450|59363e5f178f0b48e5dedc718c7f3b3e'
}

def create_user(username, email, ende, gid):        # Funktion um neue Nutzer zu erstellen.
    group_id = get_gid(gid)
    payload = json.dumps({                          # JSON mit den Informationen wird erstellt
    "userName": username,
    "email": email,
    "firstName": "Maintenance",
    "lastName": "User",
    "expiration": ende,
    "groups":[
          {
           "id": group_id
          }
        ],
    })
    print(requests.request("POST", url, headers=headers, data=payload))     # JSON Payload wird gepostet 
    return requests.request("POST", url="https://admin-api.axissecurity.com/api/v1.0/Commit", headers=headers, data={})  # Commit


