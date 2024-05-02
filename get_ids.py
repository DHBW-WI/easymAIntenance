import requests
import json
import streamlit as st




url_u = "https://admin-api.axissecurity.com/api/v1.0/Users?pageNumber=1&pageSize=150"           # API Endpunkt für Nutzerdaten
url_g = "https://admin-api.axissecurity.com/api/v1.0/Groups?pageNumber=1&pageSize=150"          # API Endpunkt für Nutzergruppendaten

payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': st.secrets["AXIS_API_KEY"],
  'Cookie': 'ax_session=1707811322.554.309.540450|59363e5f178f0b48e5dedc718c7f3b3e'
}

def get_uid(username):                                                                          # Funktion um Nutzer ID von Axis für bestimmten Nutzer abzufragen
    data = json.loads(requests.request("GET", url_u, headers=headers, data=payload).text)
    for i in data["data"]:
        if i["userName"] == username:
            return(i["id"])

def get_gid(name):                                                                              # Funktion um Gruppen ID abzufragen
    data = json.loads(requests.request("GET", url_g, headers=headers, data=payload).text)
    for i in data["data"]:
        if i["name"] == name:
            return(i["id"])

def check_u(name):                                                                              # Funktion um Existenz eines Nutzers zu prüfen 
    data = json.loads(requests.request("GET", url_u, headers=headers, data=payload).text)
    for i in data["data"]:
        if i["userName"] == name:
            return "Der Nutzer existiert"
    return "Der Nutzer existiert nicht"

def get_m():                                                                                    # Funktion um vorhandene Maschinen anzuzeigen. Alle Maschinen sind mit dem Keyword "maschine" als Gruppe in Axis angelget. 
    data = json.loads(requests.request("GET", url_g, headers=headers, data=payload).text)
    list = ""
    for i in data["data"]:
        if "maschine" in i["name"]:
            list = list + ("Name: " + i["name"] + "; Beschreibung: " + i["description"] +"| " )
    return list

