from sqlalchemy import Numeric, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, index=True)
    unit = Column(String(30), nullable=False, index=True)
    type = Column(String(30), nullable=False, index=True)
    sensor = Column(String(30), nullable=False, index=True)
    location = Column(String(100), nullable=False, index=True)
    value = Column(Numeric(3, 2))
