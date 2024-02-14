from datetime import date
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from app.models import ShiftTask


class ShiftTaskFilter(Filter):
    closing_status: Optional[bool] = None
    line: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_date: Optional[date] = None

    class Constants(Filter.Constants):
        model = ShiftTask
