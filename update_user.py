import requests
import json
from get_ids import *
import streamlit as st


url = "https://admin-api.axissecurity.com/api/v1.0/Users/"                     # API Endpunkt für User Änderungen

headers = {                                                                     # Header mit den API_Informationen
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': st.secrets["AXIS_API_KEY"],
  'Cookie': ''
}

def add_user(machine, user):                                                    # Die Funktion fügt einen bestimmten Nutzer in die passende Berechtigungsgruppe (z.B. maschine1) hinzu                                                                                          #
  uid = get_uid(user)
  payload = json.loads((requests.request("GET", url + uid, headers=headers, data={})).text)
  print(payload)
  id = get_gid(machine)
  group_id = {"id": id}
  payload["groups"].append(group_id)
  print(payload)
  print(requests.request("PUT", url + uid, headers=headers, data=json.dumps(payload)))
  return requests.request("POST", url="https://admin-api.axissecurity.com/api/v1.0/Commit", headers=headers, data={})     # Commit

def revoke_user(user):                                                          # Die Funktion entfernt den Nutzer aus der Berechtigungsgruppe
  uid = get_uid(user)
  payload = json.loads((requests.request("GET", url + uid, headers=headers, data={})).text)
  payload["groups"].pop()                                                                       # Der Gruppeneintrag wird aus den Nutzerinfos entfernt 
  print(requests.request("PUT", url + uid, headers=headers, data=json.dumps(payload)))          # Der Payload wird dann per PUT aktualisiert und der Nutzer aus der Gruppe entfernt
  return requests.request("POST", url="https://admin-api.axissecurity.com/api/v1.0/Commit", headers=headers, data={})      # Commit

