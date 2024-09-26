# easymAIntenence | Fernwartung mit Axis ZTNA

Im vorliegenden Use Case für die Fernwartung soll die Implementierung von Axis Zero Trust Network Access und die Integration eines Chatbots verdeutlichen, wie flexibel Aruba Technologien für verschiedene Anwendungsfälle angepasst werden kann. Dabei wird auch verdeutlicht, wie gut Erweiterungen von Axis SSE über die API-Schnittstelle vorgenommen werden können.

## Aufbau

## Nutzung

## Schnittstellen

### EINSTELLUNGEN OPENAI SCHNITTSTELLE
Um easymAIntenance betreiben zu können wird die API-Schnittstelle von OpenAI genutzt. Dazu wird im Kern die Funktionalität der Assistants genutzt, um einen individuell anpassbaren Chatbot erzeugen zu können. 
Dazu muss auf der API-Oberfläche von OpenAI (https://platform.openai.com/assistants) zunächst ein neuer Assistant erzeugt und mit den nötigen Anweisungen ausgestattet werden. So muss in den ‚System instructions‘ zunächst der generelle Zweck des Chatbots beschrieben werden. Für easymAIntenance wurde folgende Instruktion genutzt:

„Du bist ein Chatbot, der einem Produktionsleiter oder Produktionsmitarbeiter dabei helfen soll, anstehende Fernwartungen für Maschinen zu planen und die nötigen Berechtigungen zu vergeben. Dazu wirst du auch Functioncalling verwenden. Genauer gesagt ist deine Aufgabe von deinem Gesprächspartner folgende Informationen zu erfahren: Nutzername, Maschinenname, Startzeitpunkt und Endzeitpunkt der Fernwartung.  Diese Informationen müssen in jedem Fall vom Nutzer eingeholt werden. Optional kann auch eine E-Mail-Adresse erforderlich sein, um einen neuen Nutzeraccount zu erstellen. Frage den Nutzer vor Einrichtung der Wartung, ob alle gegebenen Informationen richtig sind und zeige ihm dazu die gesammelten Attribute für die Fernwartung. Stoße dann nach Bestätigung die nötige Funktion an. Nutze immer die exakten Informationen und achte auf Groß/Kleinschreibung.“

Darüber hinaus müssen noch einige Funktionen definiert werden, welche dann durch Function Calling aufgerufen werden können. Die zu definierenden Funktionen umfassen get_remote_instructions, add_remote_instructions, get_date, check_user und get_machines. Die Definitionen der einzelnen Funktionen befinden sich im Anhang. 
Anschließend müssen die Assistant ID (Bsp. asst_JF****************) und der OpenAI API Key in die secrets.toml Datei hinzugefügt werden. 

### EINSTELLUNGEN AXIS SSE SCHNITTSTELLE
Auf der anderen Seite ist es nötig einen Zugriff über die Schnittstelle von Axis zu gewähren. Dazu muss auf der Managementoberfläche ein neuer API-Token erstellt werden. Die Möglichkeit dazu kann unter Settings > Admin API gefunden werden. Bei der Erstellung des Tokens ist zu beachten, dass als ‚Token Permission‘ Read and Write Zugriff gewährt wird. Außerdem sollte im Abschnitt ‚Token Scope‘ der Zugriff auf Users und Groups gestattet werden. 
Auch der AXIS API Key muss anschließend in der secrets.toml Datei eingefügt werden. 


## Einrichtung in Axis SSE
Darüber hinaus müssen die im Use Case verwendeten Maschinen noch innerhalb von Axis eingerichtet werden. Dazu wird im Axis IdP eine eigene Nutzergruppe pro Maschine angelegt (Settings > Axis IdP > User Groups). 

In der Gruppenbeschreibung können weitere Hinweise zur Maschine hinterlegt werden, welche dann in der Chatoberfläche angezeigt werden können. Durch das Hinzufügen oder Entfernen aus dieser Nutzergruppe erhält ein Nutzer schließlich den Zugriff auf die Maschine. Hierfür muss schließlich noch eine Regel angelegt werden, welche allen Nutzern in der Gruppe den Zugriff auf die konkrete Anwendung gewährt. Dies kann im Bereich Policy > Rules geschehen. 

In Abbildung 3 ist zu sehen, wie die gesamte Nutzergruppe maschine1 Zugriff auf eine Destination erhält. Nachdem ein Nutzer nun zu der Nutzergruppe hinzugefügt wurde, wird die Anwendung in seinem Portal sichtbar und er erhält Zugriff. In der easymAIntenance Oberfläche muss nun der Name der Gruppe angegeben werden, um Zugriff auf die Maschine zu gewähren. 
