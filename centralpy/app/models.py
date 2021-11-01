from sqlalchemy import Numeric, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, index=True)
    value = Column(Numeric(3, 2))
