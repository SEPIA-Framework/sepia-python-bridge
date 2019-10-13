from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Any

api = FastAPI()
api_version = "0.0.3-beta"

# ---- Objects:

class Languages:
    """Available languages given as ISO 639-1 codes used by SEPIA"""
    DE = "de"
    EN = "en"

class User(BaseModel):
    """Basic information of a SEPIA user"""
    user_id: str
    user_name: dict = None
    user_roles: List[str] = None
    pref_language: str = None

class NluInput(BaseModel):
    """Input created by a SEPIA client to submit a request/answer/command etc."""
    msg_id: str = None
    text: str = ""
    text_raw: str = None
    lang: str = "en"
    context: str = None
    user: User = None
    time: int = None
    time_local: str = None
    user_location: str = None
    mood: int = None
    # last_cmd:
    # last_cmd_N:
    # input_type:
    # input_miss:
    # dialog_stage:
    client: str = None
    env: str = None
    device_id: str = None
    # connection:
    # duplex_data:
    custom_data: dict = None

class NluResult(BaseModel):
    """Result created by an 'interpretation step' of the SEPIA NLU module"""
    result: str = "fail"
    command: str = "no_result"
    certainty: float = 0.0
    best_direct_match: str = None
    normalized_text: str = None
    parameters: dict = None
    custom_data: dict = None 	#custom data defined by 'you' as needed. Will be available in services and other interpretation steps.

class ParameterResult(BaseModel):
    """Result created by a 'parameter handler'"""
    result: str = "fail"	#fail/success
    found: str = None		#if available this should be the exact match of what was found in the text
    value: str = None 		#should be a something language independent
    value_local: str = None	#should be something that can be used in a local answer
    extras: dict = None 	#custom extra info defined by 'you' as needed


# ---- Endpoints:

@api.get("/")
def hello_world():
    return {"Hello": "World"}

@api.get("/info/{info_item}")
def return_info(info_item: str, q: str = None):
    if (info_item == "server") and (q is not None) and (q == "version"):
        return {"version": api_version}
    else:
        return {"info": "unknown"}	

@api.post("/nlu/get_nlu_result")
def return_nlu_result(input: NluInput):
    return get_nlu_result(input)
	
@api.post("/nlu/get_parameter/{parameter}")
def return_parameter(parameter: str, input: NluInput):
    return get_parameter(parameter, input)


# ---- NLU:

# -- Get intent
def get_nlu_result(input: NluInput):
    """Analyze input text, find intents and optionally parameters and return NluResult."""
    #print(input)
    nluResult = find_user_intent_with_parameters(input)
    if 'custom_data' in nluResult:
        nluResult['custom_data']['source'] = "SEPIA-python-bridge"
    else:
        nluResult['custom_data'] = {
            "source": "SEPIA-python-bridge"
        }
    
    #print(nluResult)
    return NluResult(**nluResult)

# -- Get parameters (named-entities etc.)	
def get_parameter(parameter: str, input: NluInput):
    """Analyze input text to find a specific parameter (named-entity etc.) using the given parameter-handlers."""
    if parameter in parameter_handlers:
        parameterResult = parameter_handlers[parameter](input)
        return ParameterResult(**parameterResult)
    else:
        parameterResult = {
            "result": "fail"
        }
        return ParameterResult(**parameterResult)
	

# ---- Intent interpretation:

def find_user_intent_with_parameters(input: NluInput):
    """Example of a very simple intent extraction method for the SEPIA Python-Bridge demo."""
    nluResult = {}
    text = input.text_raw.lower()
    user_who_uploaded_demo_service = "uid1007" 	# adjust this ID if you used a different user to upload the python_bridge demo
    
    #Distinguish languages
    if input.lang == Languages.DE:
        #The main demo command
        if "python bridge" in text or "python brücke" in text:
            nluResult = {
                "result": "success",
                "command": (user_who_uploaded_demo_service + ".python_bridge"),
                "certainty": 1.0
            }
        #Here is another demo answer just to give you some inspiration and show one way to give a direct answer
        elif "bridge demo" in text:
            nluResult = {
                "result": "success",
                "command": "chat",
                "certainty": 0.5,
                "parameters": {
                    "reply": "Ich bin nicht sicher. Falls du die Python Brücke testen willst sag bitte 'Python bridge testen'."
                },
                "custom_data": {
                    "note": "SEPIA-python-bridge demo"
                }
            }
    else:
        #The main demo command
        if "python bridge" in text:
            nluResult = {
                "result": "success",
                "command": (user_who_uploaded_demo_service + ".python_bridge"),
                "certainty": 1.0
            }
        #Here is another demo answer just to give you some inspiration and show one way to give a direct answer
        elif "bridge demo" in text:
            nluResult = {
                "result": "success",
                "command": "chat",
                "certainty": 0.5,
                "parameters": {
                    "reply": "I'm not sure. If you want to test the Python bridge please say 'Python bridge test'."
                },
                "custom_data": {
                    "note": "SEPIA-python-bridge demo"
                }
            }
    return nluResult


# ---- Parameter handlers:

#Find coffee type
def find_parameter_code_word(input: NluInput):
    """Example of a very simple parameter extraction method for SEPIA Python-Bridge demo."""
    parameterResult = {}
    text = input.text.lower()
    
    if input.lang == Languages.DE:
        if "freund" in text:
            parameterResult = {
                "result": "success",
                "found": "freund",
                "value": "friend",
                "value_local": "Freund",
                "extras": {
                    "source": "simplest-python-matcher"
                }
            }
    else:
        if "friend" in input.text:
            parameterResult = {
                "result": "success",
                "found": "friend",
                "value": "friend",
                "value_local": "Friend",
                "extras": {
                    "source": "simplest-python-matcher"
                }
            }
    #print(parameterResult)
    return parameterResult

# ---- Parameter mapping:

#Mapping for handlers - add your parameter with name and handler method here:
parameter_handlers = {
    'code_word': find_parameter_code_word 	#This defines the '/nlu/get_parameter/code_word' path
}
