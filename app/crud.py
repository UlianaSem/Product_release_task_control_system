import datetime

from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app import models, schemas
from app.filter import ShiftTaskFilter


def create_shift_tasks(db: Session, shift_tasks: list[schemas.ShiftTaskCreate]):
    stmt = insert(models.ShiftTask).values([shift_task.dict() for shift_task in shift_tasks])
    on_update_stmt = stmt.on_conflict_do_update(
        index_elements=[models.ShiftTask.batch_date, models.ShiftTask.batch_number], set_=stmt.excluded
    )
    db.execute(on_update_stmt)
    db.commit()

    result = db.scalars(on_update_stmt.returning(models.ShiftTask), execution_options={"populate_existing": True})

    return result.fetchall()


def get_shift_task(db: Session, shift_task_id: int):
    return db.query(models.ShiftTask).filter(models.ShiftTask.id == shift_task_id).first()


def update_shift_task(db: Session, shift_task_id: int, shift_task: schemas.ShiftTaskUpdate):
    db_shift_task = db.query(models.ShiftTask).filter(models.ShiftTask.id == shift_task_id).first()

    for var, value in vars(shift_task).items():
        setattr(db_shift_task, var, value) if value else None
        if var == 'closing_status' and value is True:
            setattr(db_shift_task, 'closed_at', datetime.date.today())
        elif var == 'closing_status' and value is False:
            setattr(db_shift_task, 'closed_at', None)

    db.add(db_shift_task)
    db.commit()
    db.refresh(db_shift_task)
    return db_shift_task


def get_shift_tasks(db: Session,
                    skip: int = 0,
                    limit: int = 20,
                    shift_tasks_filter: ShiftTaskFilter = FilterDepends(ShiftTaskFilter)):
    db_shift_tasks = db.query(models.ShiftTask)
    db_shift_tasks = shift_tasks_filter.filter(db_shift_tasks)
    return db_shift_tasks.offset(skip).limit(limit).all()
