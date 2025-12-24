from fastapi import FastAPI, Path, HTTPException, Query
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

@app.get("/view/{patient_id}")
async def get_patient(patient_id: str = Path(..., description="The ID of the patient to get", example="P001")):
    data = load_data()
    if patient_id in data :
            return data[patient_id]
    raise HTTPException(status_code=404, detail={"error": "Patient not found"})

@app.get("/sort")
async def sort_patients(sort_by: str = Query(..., description="The attribute to sort by height, weight, bmi"), order: str = Query("asc", description="Sort order: asc or desc")):

    valid_fileds= {"height", "weight", "bmi"}
    
    if sort_by not in valid_fileds:
        raise HTTPException(status_code=400, detail={"error": f"Invalid sort_by field. Must be one of {valid_fileds}"}) 
    
    if order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail={"error": "Invalid order. Must be 'asc' or 'desc'"})
    
    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data