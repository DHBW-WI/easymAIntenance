import json
import time
import datetime as dt
import threading

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from openai import OpenAI

from update_user import add_user
from new_user import create_user
from get_ids import check_u
from get_ids import get_m
from time_manager import schedule_job



# Prerequisits


st.set_page_config(                     # Konfiguration der Seite (Titel, Icon, etc. )
    page_title="easy mAIntenance",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Authentication

with open('config.yaml') as file:           # Laden der Anmeldedaten
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(        
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

authenticator.login()       

if st.session_state["authentication_status"] is False:          # Prüfen der Login Informationen 
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
        
    # OpenAI

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])       # Laden des API-Key und erstellen eines OpenAI-Client

    assistant_id = st.secrets["OPENAI_ASSISTANT_ID"]

    assistant_state = "assistant"
    thread_state = "thread"
    conversation_state = "conversation"
    last_openai_run_state = "last_openai_run"


    user_msg_input_key = "input_user_msg"

    # Session State Setup

    if (assistant_state not in st.session_state) or (thread_state not in st.session_state):
        st.session_state[assistant_state] = client.beta.assistants.retrieve(assistant_id)
        st.session_state[thread_state] = client.beta.threads.create()

    if conversation_state not in st.session_state:
        st.session_state[conversation_state] = []

    if last_openai_run_state not in st.session_state:
        st.session_state[last_openai_run_state] = None


    # Tools (In der OpenAI Oberfläche definierte Funktionen)

    def get_remote_instructions(ip, user, start, ende):         # Funktionsaufuruf um die Berechtigungen in Axis einzurichter (bestehender Nutzer)
        print(ip, user, start, ende)
        threading.Thread(target=schedule_job, args=(start, ende, user, ip)).start()
        return "Success"
        

    def add_remote_instructions(ip, user, start, ende, email):          # Funktionsaufuruf um die Berechtigungen in Axis einzurichter (neuer Nutzer)
        print(ip, user, start, ende, email)
        print(create_user(user, email, ende, ip))
        return "Success"

    def get_date():         # Funktionsaufruf um das aktuelle Datum und die Zeit für GPT bereitzustellen
        print((dt.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
        now = (dt.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps(now)
    
    def check_user(user):       # Funktionsaufruf, um Existenz eines Nutzers zu prüfen
        return check_u(user)

    def get_machines():         # Funktionsaufruf, um Liste der vorhandenen Maschinen zu bekommen
        return get_m()




    tool_to_function = {        # Definieren und festlegen der Funktionsnamen, die für GPT nutzbar sind
        "get_remote_instructions": get_remote_instructions,
        "add_remote_instructions": add_remote_instructions,
        "get_date": get_date,
        "check_user": check_user,
        "get_machines": get_machines,
    }

    # Helpers


    def get_assistant_id():                                     # Assistant ID abrufen
        return st.session_state[assistant_state].id


    def get_thread_id():                                        # Thread ID abrufen
        return st.session_state[thread_state].id


    def get_run_id():                                           # Run ID abrufen
        return st.session_state[last_openai_run_state].id


    def on_text_input(status_placeholder):
        """Callback method for any chat_input value change
        """
        if st.session_state[user_msg_input_key] == "":
            return

        client.beta.threads.messages.create(
            thread_id=get_thread_id(),
            role="user",
            content=st.session_state[user_msg_input_key],
        )
        st.session_state[last_openai_run_state] = client.beta.threads.runs.create(
            assistant_id=get_assistant_id(),
            thread_id=get_thread_id(),
        )

        completed = False

        # Generate answer
        with status_placeholder.status("Computing Assistant answer") as status_container:
            st.write(f"Launching run {get_run_id()}")

            # Schleife, die läuft, bis der Lauf abgeschlossen ist
            while not completed:
                run = client.beta.threads.runs.retrieve(
                    thread_id=get_thread_id(),
                    run_id=get_run_id(),
                )

                if run.status == "requires_action":         # Prüft, ob der Lauf eine Aktion benötigt
                    tools_output = []
                    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                        f = tool_call.function
                        print(f)                            # Druck zum Debuggen
                        f_name = f.name
                        f_args = json.loads(f.arguments)

                        st.write(f"Launching function {f_name} with args {f_args}")
                        tool_result = tool_to_function[f_name](**f_args)
                        tools_output.append(
                            {
                                "tool_call_id": tool_call.id,
                                "output": tool_result,
                            }
                        )

                    # Gibt die gesammelten Ergebnisse aus
                    st.write(f"Will submit {tools_output}")
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=get_thread_id(),
                        run_id=get_run_id(),
                        tool_outputs=tools_output,
                    )


                # Überprüft, ob der Lauf abgeschlossen ist
                if run.status == "completed":
                    st.write(f"Completed run {get_run_id()}")
                    status_container.update(label="Assistant is done", state="complete")
                    completed = True

                else:
                    time.sleep(0.1)

        # Speichert den aktuellen Gesprächsstatus im Session State
        st.session_state[conversation_state] = [
            (m.role, m.content[0].text.value)
            for m in client.beta.threads.messages.list(get_thread_id()).data
        ]

    # Funktion zum Zurücksetzen des Threads
    def on_reset_thread():
        # Löscht den aktuellen Thread
        client.beta.threads.delete(get_thread_id())
        # Erstellt einen neuen Thread und speichert ihn im Session State
        st.session_state[thread_state] = client.beta.threads.create()
        # Setzt den Gesprächszustand zurück
        st.session_state[conversation_state] = []
        st.session_state[last_openai_run_state] = None #  Setzt den letzten OpenAI-Run-Zustand zurück


    
    # Debugging sidebar

    with st.sidebar:
        st.header("Debug")
        st.write(st.session_state.to_dict())

        st.button("Reset Thread", on_click=on_reset_thread)

    # main

    st.title("⚙️easy m:red[AI]ntenance")
    left_col, right_col = st.columns(2)

                                # Linke Seite mit Chat        
    with st.container():
        for role, message in reversed(st.session_state[conversation_state]):
            with st.chat_message(role):
                st.write(message)
    status_placeholder = st.empty()

    st.chat_input(                              # Input Feld definieren
        placeholder="...",
        key=user_msg_input_key,
        on_submit=on_text_input,
        args=(status_placeholder,),
        )    


