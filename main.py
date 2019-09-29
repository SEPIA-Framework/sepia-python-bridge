from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Any

api = FastAPI()
api_version = "0.0.1-beta"

# ---- Objects:

class Languages:
    """Available languages given as ISO 639-1 codes used by SEPIA"""
    DE = "de"
    EN = "en"

class User(BaseModel):
    """Basic information of a SEPIA user"""
    userId: str
    userName: dict = None
    userRoles: List[str] = None
    prefLanguage: str = None

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
    bestDirectMatch: str = None
    normalizedText: str = None
    parameters: dict = None

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
	
# ---- NLU:

def get_nlu_result(input: NluInput):
    """Analyze input text, find intents and optionally parameters and return NluResult."""
    #print(input)
    nluResult = {}
    
    #Example of a very simple NLU method:
    if input.lang == Languages.DE:
        if "hallo" in input.text:
            nluResult = {
                "result": "success",
                "command": "chat",
                "certainty": 0.9,
                "parameters": {
                    "type": "greeting"
                }
            }
    else:
        if "hello" in input.text:
            nluResult = {
                "result": "success",
                "command": "chat",
                "certainty": 0.9,
                "parameters": {
                    "type": "greeting"
                }
            }
    #print(nluResult)
    return NluResult(**nluResult)
