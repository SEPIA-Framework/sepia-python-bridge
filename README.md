# SEPIA Python Bridge Server
The Python bridge-server connects other SEPIA components to the Python runtime. 
Via the [FastAPI framework](https://fastapi.tiangolo.com) you can create HTTP endpoints that can be integrated into your SEPIA Java backend for example to extend the NLU module.
  
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

