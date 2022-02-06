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

The NLU interpretation chain of SEPIA consists of several consecutive processes that analyze the user input until the best NLU result is found.  
To integrate the Python Bridge into the NLU chain follow these steps:
- Open the properties file of your SEPIA assist server (usually: `~/SEPIA/sepia-assist-server/Xtensions/assist.custom.properties`) or use the Control-HUB to modify the line that starts with: `nlu_interpretation_chain=...`.
- Each entry in `nlu_interpretation_chain` is one 'step' of the chain and steps are executed from left to right. Choose a good spot for your own Python NLU.
- Where exactly you put it is up to you but a good spot is between `getPersonalCommand` (custom user commands defined via the Teach-UI or SDK) and `getKeywordAnalyzerResult` (the most flexible NLU step).
- If you're running the Python bridge server on the same machine as SEPIA-Home add it to the chain like this: `...,WEB:http\://127.0.0.1\:20731/nlu/get_nlu_result,...`.
- Don't forget to restart your server.

## Use the bridge for custom micro-services

To use the Python Bridge as server for custom micro-services you can simply import your libraries and add new HTTP endpoints at the top of the main script. See example:
```
# -- HTTP GET with 'q' as URL parameter
@api.get("/my-service")
def my_service(q: str = None):
    if q is not None:
        # implement your logic here
        return {"reply": "to be implemented"}
    else:
        raise HTTPException(status_code=400, detail="Missing query parameter 'q'")
```

You can then access the endpoint via a simple HTTP GET call for example in custom smart-services via SEPIA Java SDK:
```
JSONObject response = Connectors.apacheHttpGETjson(
	"http://127.0.0.1:20731/my-service/?q=" + URLEncoder.encode("my question", "UTF-8")
);
```
