from fastapi import FastAPI
import json

app = FastAPI()
@app.get("/")
async def read_root():
    return {"Hello": "World"}

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)

        return data
    
@app.get("/view")
async def get_patients():
    data = load_data()
    return data