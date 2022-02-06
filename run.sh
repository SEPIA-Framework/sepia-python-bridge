#!/bin/bash
uvicorn main:api --host 0.0.0.0 --port 20731 --log-level info --reload
