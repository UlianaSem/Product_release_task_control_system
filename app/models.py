from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, UniqueConstraint

from app.database import Base


class ShiftTask(Base):
    __tablename__ = "shift_tasks"

    id = Column(Integer, primary_key=True, index=True)
    closing_status = Column(Boolean, nullable=False)
    closed_at = Column(Date, nullable=True)
    submission_task_shift = Column(String(50), nullable=False)
    line = Column(String(10), nullable=False)
    shift = Column(String(10), nullable=False)
    brigade = Column(String(50), nullable=False)
    batch_number = Column(Integer, nullable=False)
    batch_date = Column(Date, nullable=False)
    nomenclature = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)
    identifier = Column(String(10), nullable=False)
    begin_shift_time = Column(DateTime, nullable=False)
    end_shift_time = Column(DateTime, nullable=False)

    UniqueConstraint("batch_number", "batch_date", name="batch")
