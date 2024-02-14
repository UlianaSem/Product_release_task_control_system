from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class UniqueCode(BaseModel):
    id: int
    unique_code: str


class ShiftTaskCreate(BaseModel):
    closing_status: bool = Field(validation_alias='СтатусЗакрытия')
    submission_task_shift: str = Field(validation_alias='ПредставлениеЗаданияНаСмену')
    line: str = Field(validation_alias='Линия')
    shift: str = Field(validation_alias='Смена')
    brigade: str = Field(validation_alias='Бригада')
    batch_number: int = Field(validation_alias='НомерПартии')
    batch_date: date = Field(validation_alias='ДатаПартии')
    nomenclature: str = Field(validation_alias='Номенклатура')
    code: str = Field(validation_alias='КодЕКН')
    identifier: str = Field(validation_alias='ИдентификаторРЦ')
    begin_shift_time: datetime = Field(validation_alias='ДатаВремяНачалаСмены')
    end_shift_time: datetime = Field(validation_alias='ДатаВремяОкончанияСмены')


class ShiftTaskUpdate(BaseModel):
    closing_status: Optional[bool] = None
    submission_task_shift: Optional[str] = None
    line: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_number: Optional[int] = None
    batch_date: Optional[date] = None
    nomenclature: Optional[str] = None
    code: Optional[str] = None
    identifier: Optional[str] = None
    begin_shift_time: Optional[datetime] = None
    end_shift_time: Optional[datetime] = None


class ShiftTask(ShiftTaskUpdate):
    id: int
    closed_at: Optional[date]
    unique_codes: Optional[list[UniqueCode]]

    class Config:
        from_attributes = True


class ShiftTaskWithUniqueCodeCreate(BaseModel):
    unique_code: str = Field(validation_alias='УникальныйКодПродукта')
    batch_number: int = Field(validation_alias='НомерПартии')
    batch_date: date = Field(validation_alias='ДатаПартии')


class ShiftTaskWithUniqueCode(BaseModel):
    id: int
    unique_code: str
    shift_task: int
    is_aggregated: bool
    aggregated_at:  Optional[datetime]

    class Config:
        from_attributes = True


class AggregateModel(BaseModel):
    shift_task_id: int
    unique_code: str
