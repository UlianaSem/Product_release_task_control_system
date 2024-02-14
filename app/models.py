from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

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

    unique_codes = relationship("ProductUniqueCode")

    __table_args__ = (
        UniqueConstraint("batch_number", "batch_date", name="batch"),
    )


class ProductUniqueCode(Base):
    __tablename__ = "unique_codes"

    id = Column(Integer, primary_key=True, index=True)
    unique_code = Column(String(30), nullable=False)
    shift_task = Column(Integer, ForeignKey('shift_tasks.id', ondelete='CASCADE', comment="CASCADE"), index=True)
    is_aggregated = Column(Boolean, default=False)
    aggregated_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("unique_code", name="code"),
    )
