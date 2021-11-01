import datetime
import os
import pathlib

import uvicorn
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from pydantic import BaseModel
from models import Measurement, Base


class TempSensReport(BaseModel):
    value: float


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
async def home(request: Request):
    data = {"text": "hi"}
    return templates_dir.TemplateResponse("dashboard.html", {"request": request})


@app.post("/api/temperature/")
async def temperature_measurement(temp_report: TempSensReport, background_tasks=BackgroundTasks, db: Session = Depends(get_db)):
    """
    api to post measurements to

    :param temp_report:
    :return:
    """
    measurement = Measurement()
    measurement.value = temp_report.value
    db.add(measurement)
    db.commit()
    return {"data": "data"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=2)
