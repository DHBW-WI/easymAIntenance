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
from time_manager import get_j


#######################################
# PREREQUISITES
#######################################

st.set_page_config(
    page_title="easy mAIntenance",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#######################################
# AUTHENTICATION
#######################################

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
        
    #######################################
    # OPENAI
    #######################################

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    assistant_id = st.secrets["OPENAI_ASSISTANT_ID"]

    assistant_state = "assistant"
    thread_state = "thread"
    conversation_state = "conversation"
    last_openai_run_state = "last_openai_run"


    user_msg_input_key = "input_user_msg"

        #######################################
        # SESSION STATE SETUP
        #######################################

    if (assistant_state not in st.session_state) or (thread_state not in st.session_state):
        st.session_state[assistant_state] = client.beta.assistants.retrieve(assistant_id)
        st.session_state[thread_state] = client.beta.threads.create()

    if conversation_state not in st.session_state:
        st.session_state[conversation_state] = []

    if last_openai_run_state not in st.session_state:
        st.session_state[last_openai_run_state] = None


        #######################################
        # TOOLS AUFRUFEN
        #######################################

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

    def get_jobs():             # Funktionsaufruf, um Liste der gerade eingerichteten Fernwartungen zu bekommen (funktioniert noch nicht)
        return get_j()


    tool_to_function = {        # "Festlegen" der Funktionsnamen für GPT
        "get_remote_instructions": get_remote_instructions,
        "add_remote_instructions": add_remote_instructions,
        "get_date": get_date,
        "check_user": check_user,
        "get_machines": get_machines,
        "get_jobs": get_jobs
    }

    #######################################
    # HELFER
    #######################################


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

        # Antwort generieren
        with status_placeholder.status("Computing Assistant answer") as status_container:
            st.write(f"Launching run {get_run_id()}")

            while not completed:
                run = client.beta.threads.runs.retrieve(
                    thread_id=get_thread_id(),
                    run_id=get_run_id(),
                )

                if run.status == "requires_action":
                    tools_output = []
                    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                        f = tool_call.function
                        print(f)
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
                    st.write(f"Will submit {tools_output}")
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=get_thread_id(),
                        run_id=get_run_id(),
                        tool_outputs=tools_output,
                    )

                if run.status == "completed":
                    st.write(f"Completed run {get_run_id()}")
                    status_container.update(label="Assistant is done", state="complete")
                    completed = True

                else:
                    time.sleep(0.1)

        st.session_state[conversation_state] = [
            (m.role, m.content[0].text.value)
            for m in client.beta.threads.messages.list(get_thread_id()).data
        ]


    def on_reset_thread():
        client.beta.threads.delete(get_thread_id())
        st.session_state[thread_state] = client.beta.threads.create()
        st.session_state[conversation_state] = []
        st.session_state[last_openai_run_state] = None


    #######################################
    # SIDEBAR
    #######################################

    with st.sidebar:
        st.header("Debug")
        st.write(st.session_state.to_dict())

        st.button("Reset Thread", on_click=on_reset_thread)

    #######################################
    # MAIN
    #######################################

    st.title("⚙️easy m:red[AI]ntenance")
    left_col, right_col = st.columns(2)

    with left_col:                              # Linke Seite mit Chat        
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

    with right_col:                             # Rechte Seite mit Bild
        st.image('network.png')
        

  