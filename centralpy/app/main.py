import datetime
import os
import pathlib

import uvicorn
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from pydantic import BaseModel
from models import Measurement, Base


class TempSensReport(BaseModel):
    value: float
    time: datetime.datetime
    sensor_type: str
    unit: str
    location: str


class CO2SensReport(BaseModel):
    value: float
    time: datetime.datetime
    sensor_type: str
    unit: str
    location: str


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app = FastAPI()
Base.metadata.create_all(bind=engine)
this_file_dir = pathlib.Path(__file__).parent.resolve()

templates_dir = Jinja2Templates(directory=os.path.join(this_file_dir, "templates"))


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    measurements = db.query(Measurement).all()
    return templates_dir.TemplateResponse("dashboard.html", {"request": request, "measurements": measurements})


@app.post("/api/temperature/")
async def temperature_measurement(temp_report: TempSensReport, db: Session = Depends(get_db)):
    """
    api to post measurements to

    :param temp_report: post temperature in centi degrees (27.6 degrees Celsius becomes 2760)
    :param db:
    :return:
    """
    measurement = Measurement()
    measurement.value = temp_report.value
    measurement.time = temp_report.time
    measurement.sensor = temp_report.sensor_type
    measurement.unit = temp_report.unit
    measurement.location = temp_report.location
    measurement.type = "temperature"
    db.add(measurement)
    db.commit()
    return {"data": "data"}


@app.post("/api/co2/")
async def temperature_measurement(co2_report: CO2SensReport, db: Session = Depends(get_db)):
    """
    api to post measurements to

    :param co2_report: post co2 in ppm
    :param db:
    :return:
    """
    measurement = Measurement()
    measurement.value = co2_report.value
    measurement.time = co2_report.time
    measurement.sensor = co2_report.sensor_type
    measurement.unit = co2_report.unit
    measurement.location = co2_report.location
    measurement.type = "co2"
    db.add(measurement)
    db.commit()
    return {"data": "data"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=2)
