from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
from pathlib import Path
import os
import time

app = FastAPI()

class TimeRequest(BaseModel):
    time_string: str

@app.post("/time/")
async def receive_time(request: Request):
    data = await request.json()
    time_string = data.get("time_string")
    if time_string:
        save_to_json({"received_time": time_string})
        return {"received_time": time_string}
    return {"error": "Invalid time string"}

def save_to_json(data):
    file_path = "times.json"
    try:
        with open(file_path, "w") as file:
            json.dump([data], file, indent=4)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        return
    

