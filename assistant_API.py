import json
import time
import datetime as dt

import streamlit as st

from openai import OpenAI

from update_user import add_user
from new_user import create_user
from get_ids import check_u
#from time_manager import schedule_job

#######################################
# PREREQUISITES
#######################################

st.set_page_config(
    page_title="easy mAIntenance",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
# TOOLS SETUP
#######################################

def get_remote_instructions(ip, user, start, ende):
    print(ip, user, start, ende)
    #print(add_user(ip, user))
    #schedule_job(start, ende, user)
    return str(add_user(ip, user))

def add_remote_instructions(ip, user, start, ende, email):
    print(ip, user, start, ende, email)
    print(create_user(user, email, ende, ip))
    return "Success"

def get_date():
    print(dt.datetime.now())
    now = dt.datetime.now()
    return json.dumps(now.isoformat())
    
def check_user(user):
    return check_u(user)

tool_to_function = {
    "get_remote_instructions": get_remote_instructions,
    "add_remote_instructions": add_remote_instructions,
    "get_date": get_date,
    "check_user": check_user
}

#######################################
# HELPERS
#######################################


def get_assistant_id():
    return st.session_state[assistant_state].id


def get_thread_id():
    return st.session_state[thread_state].id


def get_run_id():
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

    # Polling
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

st.title("⚙️ easy mAIntenance")

with st.container():
    for role, message in reversed(st.session_state[conversation_state]):
        with st.chat_message(role):
            st.write(message)
status_placeholder = st.empty()


    

st.chat_input(
    placeholder="...",
    key=user_msg_input_key,
    on_submit=on_text_input,
    args=(status_placeholder,),
)