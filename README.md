# SEPIA Python Bridge Server
The Python bridge-server connects other SEPIA components to the Python runtime. 
Via the [FastAPI framework](https://fastapi.tiangolo.com) you can create HTTP endpoints that can be integrated into your SEPIA Java backend for example to extend the NLU (natural-language-understanding) module.
  
[BETA - UNDER CONSTRUCTION]

## Installation

Requirements:
* Python 3.6+

```
pip install fastapi
pip install uvicorn
git clone https://github.com/SEPIA-Framework/sepia-python-bridge.git
```

## Run server

From bridge-server folder call:
```
uvicorn main:api --host 0.0.0.0 --port 20731 --log-level info --reload
```

More command-line settings can be found [here](https://www.uvicorn.org/settings/) (e.g. `--no-access-log`).

## Integrate the server into SEPIA's NLU chain

To use the Python bridge with your SEPIA-Home installation open the properties file of your SEPIA assist server (usually found at `~/SEPIA/sepia-assist-server/Xtensions/assist.custom.properties`) or use the Control-HUB to modify the line that starts with: `nlu_interpretation_chain=...`.
This line represents the NLU interpretation chain of SEPIA. Each entry is one 'step' of the chain and steps are executed from left to right until the best NLU result is found.  
If you're running the Python bridge server on the same machine as SEPIA-Home you can add it to the chain like this: `...,WEB:http\://127.0.0.1\:20731/nlu/get_nlu_result,...`.
Where you put it exactly is up to you but I'd recommend to place it between `getPublicDbSentenceMatch` (the step that takes care of custom commands defined via the Teach-UI) and `getKeywordAnalyzerResult` (the most flexible NLU step) too keep most of SEPIA's default functions intact ;-) .
