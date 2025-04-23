from fastapi import FastAPI
from pydantic import BaseModel
from ml.train import predict
import numpy
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
print("NumPy version:", numpy.__version__)
class RideRequest(BaseModel):
    Number_of_Riders: int
    Number_of_Drivers: int
    Location_Category: str
    Customer_Loyalty_Status: str
    Number_of_Past_Rides: int
    Average_Ratings: float
    Time_of_Booking: str
    Vehicle_Type: str
    Expected_Ride_Duration: int

@app.post("/predict")
def predict_ride(data: RideRequest):
    prediction = predict(data.dict())
    return {"predicted_ride_cost": prediction}

