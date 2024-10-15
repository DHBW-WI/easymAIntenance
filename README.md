# easymAIntenence | Remote maintenance with Axis ZTNA

In this use case for remote maintenance, the implementation of Axis Zero Trust Network Access and the integration of a chatbot are intended to illustrate how flexibly Aruba technologies can be adapted for various use cases. It also illustrates how well extensions to Axis SSE can be made via the API interface.

## Interfaces

### OPENAI 
The API interface from OpenAI is used to operate easymAIntenance. The core functionality of the assistants is used to create a customizable chatbot. 
To do this, a new assistant must first be created on the OpenAI API interface (https://platform.openai.com/assistants) and provided with the necessary instructions. The general purpose of the chatbot must first be described in the 'System instructions'. The following instruction was used for easymAIntenance:

“You are a chatbot that will help a production manager or production employee to plan upcoming remote maintenance for machines and assign the necessary authorizations. You will also use function calling to do this. More specifically, your task is to find out the following information from your conversation partner: User name, machine name, start time and end time of the remote maintenance.  This information must always be obtained from the user. Optionally, an e-mail address may also be required to create a new user account. Before setting up the maintenance, ask the user whether all the information provided is correct and show them the collected attributes for the remote maintenance. Then initiate the necessary function after confirmation. Always use the exact information and pay attention to capitalization.”

In addition, some functions must be defined, which can then be called by function calling. The functions to be defined include get_remote_instructions, add_remote_instructions, get_date, check_user and get_machines. The definitions of the individual functions can be found in the appendix. 
The assistant ID (e.g. asst_JF****************) and the OpenAI API key must then be added to the secrets.toml file. 

### AXIS SSE
On the other hand, it is necessary to grant access via the Axis interface. To do this, a new API token must be created on the management interface. The option to do this can be found under Settings > Admin API. When creating the token, make sure that Read and Write access is granted as 'Token Permission'. In addition, access to users and groups should be permitted in the 'Token Scope' section. 
The AXIS API key must also be added to the secrets.toml file. 


## Einrichtung in Axis SSE
In addition, the machines used in the use case must still be set up within Axis. To do this, a separate user group is created for each machine in the Axis IdP (Settings > Axis IdP > User Groups). 

Further information about the machine can be stored in the group description, which can then be displayed in the chat interface. By adding or removing a user from this user group, a user is finally granted access to the machine. Finally, a rule must be created for this, which grants all users in the group access to the specific application. This can be done in the Policy > Rules area. 


## Use
To access and present the use case, the following details must be observed. The heart of the use case is the chatbot interface, which can be started with the following instruction: 
```python3 -m streamlit run assistant_API.py```
The information requested by the chatbot includes: 
- User name: To grant access, a user account created in the Axis IdP is of course required. The exact user name should be specified.
- Machine name: A “machine name” is also required. This represents the existing machines and includes “maschine1” and “maschine2” in the current structure. 
- Start time: The start time of the maintenance must be specified. This can be realized by relative (“Today in 10 minutes”; “In two hours”), as well as by absolute specifications (“24.04.2024 at 12 noon”).
- End time: The end time of the maintenance must also be specified. This can be realized by relative (“Today in 10 minutes”; “In two hours”), as well as by absolute specifications (“24.04.2024 at 12 noon”).
- (e-mail address): If a new account has to be created for maintenance, a valid e-mail address must be entered. The link to the password assignment for the account will be sent to this address. Important: No other user may be created in the Axis IdP under the e-mail address. 


## Best Practices
The system can be operated quite intuitively. The chatbot is designed to request all relevant information (see section 4) from the user and ultimately have it checked again. Nevertheless, there are a few general points to bear in mind when interacting with the chatbot:
- __Clear communication:__ It is advisable to start the dialog with a declaration of intent. This is not absolutely necessary, but it makes the process easier and makes the prototype look even better. An initial request in the style of “Can you help me set up remote maintenance?” or “I would like to set up remote maintenance” makes the process easier.

- **Precise communication:** Another aspect is precise communication with the system. It is very important to specify the relevant information precisely. Important: To ensure a smooth process, the exact machine name “maschine1” should be used, taking lower case into account. 						The spelling of the user name should also be exact. However, the system can help with this, as it checks on request whether a user exists in the Axis IdP.

- Answering questions:** In addition, the chatbot's queries should be taken into account and the collected attributes should be checked by the user at the end of the information collection process. The chatbot only assigns rights after the attributes have been checked. 

