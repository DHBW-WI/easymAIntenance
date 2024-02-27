import os
from openai import OpenAI
import json
import re
from update_user import add_user
from new_user import create_user
#from time_manager import schedule_job

client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_remote_instructions",
            "description": "Parameter für einen Fernzugriff auf eine IP-Adresse",
            "parameters": {
                "type": "object",
                "properties": {
                    "ip-adresse": {
                        "type": "string",
                        "description": "Die IP-Adresse oder die Bezeichnung der fernzuwartenden Maschine.",
                    },
                    "user": {
                        "type": "string",
                        "description": "Username des freizuschaltenden Nutzers, e.g. contractor",
                    },
                    "email": {
                        "type": "string",
                        "description": "E-Mail Adresse eines neuen, freizuschaltenden Nutzers. Achte darauf, dass die Adresse ein @ Symbol beinhaltet. Dieses Feld ist ausdrücklich optional, e.g. Test@test.com",
                    },
                    "start": {
                        "type": "string",
                        "description": "Startzeitpunkt ab dem der Zugriff gewährt werden soll. Wenn kein Jahr definiert wird, nutze das Jahr 2024. Nutze dabei das Zahlenformat nach ISO 8601: YYYY-MM-DDThh:mm:ss, e.g. 2024-02-15T19:16:ss",
                    },
                    "ende": {
                        "type": "string",
                        "description": "Endzeitpunkt bis zu dem der Zugriff gewährt werden soll. Wenn kein Jahr definiert wird, nutze das Jahr 2024. Nutze dabei das Zahlenformat nach ISO 8601: YYYY-MM-DDThh:mm:ss, e.g. 2024-02-15T19:16:00",
                    },
                },
                "required": ["ip-adresse","user","start","ende"],
            },
        }
    }
]

#user_prompt = "Gib dem Nutzer maintenance_user von heute bis zum 18.2 um 9:26 Uhr. Zugriff auf die Maschine remote_maintenance. Erstelle dazu den benutzer mit der email test1@test.com"
#user_prompt = input("Anweisung eingeben: ")
#user_prompt = ""

def call_gpt(user_prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "Generate JSON response"},
            {"role": "user", "content": user_prompt}
        ],
        # Add function calling
        tools=tools,
        tool_choice="auto",  # specify the function call
    )

    # It automatically fills the arguments with correct info based on the prompt
    # Note: the function does not exist yet

    data = str(completion.choices[0].message)

    start_index = data.find("{")
    end_index = data.rfind("}") + 1
    json_data = data[start_index:end_index]
    json_data = json_data.replace("\\n", '')

    # Laden des JSON-Strings
    parsed_data = json.loads(json_data)

    # Extrahieren des Wertes der Schlüssel
    print("Wert des Keys 'user':", parsed_data.get("user"))
    print("Wert des Keys 'ip':", parsed_data.get("ip-adresse"))
    print("Wert des Keys 'start':", parsed_data.get("start"))
    print("Wert des Keys 'ende':", parsed_data.get("ende"))
    print("Wert des Keys 'email':", parsed_data.get("email"))

    #Email validieren
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    #Prüfung ob neuer User erstell wird
    if parsed_data.get("email") is None:
        print("Search User")
        print(add_user(parsed_data.get("ip-adresse"), parsed_data.get("user")))
        #schedule_job(parsed_data.get("start"), parsed_data.get("ende"), parsed_data.get("user"))
    elif validate_email(parsed_data.get("email")) == True:
        print("Create User")
        print(create_user(parsed_data.get("user"), parsed_data.get("email"), parsed_data.get("ende"), parsed_data.get("ip-adresse")))
    else: 
        print("No valid E-Mail adress")
