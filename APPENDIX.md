```
Definition get_remote_instructions

{
  "name": "get_remote_instructions",
  "description": "Parameter für einen Fernzugriff auf eine IP-Adresse",
  "strict": false,
  "parameters": {
    "type": "object",
    "properties": {
      "ip": {
        "type": "string",
        "description": "Die IP oder die Bezeichnung der fernzuwartenden Maschine."
      },
      "user": {
        "type": "string",
        "description": "Username des freizuschaltenden Nutzers, e.g. contractor. Der Nutzername muss in jedem Fall eingeholt werden."
      },
      "start": {
        "type": "string",
        "description": "Startzeitpunkt ab dem der Zugriff gewährt werden soll. Wenn kein Jahr definiert wird, nutze das Jahr 2024. Nutze dabei das Zahlenformat nach ISO 8601: YYYY-MM-DDThh:mm:ss, e.g. 2024-02-15T19:16:00"
      },
      "ende": {
        "type": "string",
        "description": "Endzeitpunkt bis zu dem der Zugriff gewährt werden soll. Wenn kein Jahr definiert wird, nutze das Jahr 2024. Nutze dabei das Zahlenformat nach ISO 8601: YYYY-MM-DDThh:mm:ss, e.g. 2024-02-15T19:16:00"
      }
    },
    "required": [
      "ip",
      "user",
      "start",
      "ende"
    ]
  }
}

Definition add_remote_instructions
{
  "name": "add_remote_instructions",
  "description": "Parameter für einen Fernzugriff auf eine IP-Adresse. Die Funktion wird nur genutzt, wenn ein neuer Account mit E-Mail erstellt wird",
  "strict": false,
  "parameters": {
    "type": "object",
    "properties": {
      "ip": {
        "type": "string",
        "description": "Die IP oder die Bezeichnung der fernzuwartenden Maschine."
      },
      "user": {
        "type": "string",
        "description": "Username des freizuschaltenden Nutzers, e.g. contractor"
      },
      "email": {
        "type": "string",
        "description": "E-Mail Adresse eines neuen, freizuschaltenden Nutzers. Achte darauf, dass die Adresse ein @ Symbol beinhaltet. Dieses Feld ist ausdrücklich optional, e.g. Test@test.com"
      },
      "start": {
        "type": "string",
        "description": "Startzeitpunkt ab dem der Zugriff gewährt werden soll. Wenn kein Jahr definiert wird, nutze das Jahr 2024. Nutze dabei das Zahlenformat nach ISO 8601: YYYY-MM-DDThh:mm:ss, e.g. 2024-02-15T19:16:ss. Diese Information muss immer abgefragt werden"
      },
      "ende": {
        "type": "string",
        "description": "Endzeitpunkt bis zu dem der Zugriff gewährt werden soll. Wenn kein Jahr definiert wird, nutze das Jahr 2024. Nutze dabei das Zahlenformat nach ISO 8601: YYYY-MM-DDThh:mm:ss, e.g. 2024-02-15T19:16:00. Diese Information muss immer abgefragt werden"
      }
    },
    "required": [
      "ip",
      "user",
      "start",
      "ende",
      "email"
    ]
  }
}

Definition get_date
{
  "name": "get_date",
  "description": "Diese Funktion gibt das Datum und die Uhrzeit des heutigen Tages zurück. Sie kann genutzt werden um Fernwartungen zu planen und Zeitangaben nachzuvollziehen",
  "strict": false,
  "parameters": {
    "required": [],
    "type": "object",
    "properties": {}
  }
}

Definition check_user
{
  "name": "check_user",
  "description": "Diese Funktion bietet die Möglichkeit zu prüfen, ob ein bestimmter User oder Nutzer schon vergeben und angelegt ist. Die Rückmeldung True bedeutet, dass der Nutzer bereits existiert.",
  "strict": false,
  "parameters": {
    "type": "object",
    "properties": {
      "user": {
        "type": "string",
        "description": "Username des zu prüfenden Nutzers, e.g. contractor"
      }
    },
    "required": [
      "user"
    ]
  }
}

Definition get_machines
{
  "name": "get_machines",
  "description": "Diese Funktion gibt alle für eine Fernwartung verfügbaren Maschinen zurück. Sie kann genutzt werden um Fernwartungen zu planen und dem Nutzer auskunft zu geben. Beachte unbedingt Groß- und Kleinschreibung bei en Maschinennamen",
  "strict": false,
  "parameters": {
    "required": [],
    "type": "object",
    "properties": {}
  }
}
