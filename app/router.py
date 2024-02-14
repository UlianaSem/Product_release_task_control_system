from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app import schemas, crud, database, services
from app.filter import ShiftTaskFilter

shift_tasks_router = APIRouter(prefix="/shift_task", tags=['Shift tasks'])


@shift_tasks_router.post('/', response_model=list[schemas.ShiftTask])
def create_shift_tasks(shift_tasks: list[schemas.ShiftTaskCreate], db: Session = Depends(database.get_db)):
    return crud.create_shift_tasks(db=db, shift_tasks=shift_tasks)


@shift_tasks_router.get('/{shift_task_id}', response_model=schemas.ShiftTask)
def get_task(shift_task_id: int, db: Session = Depends(database.get_db)):
    db_shift_task = crud.get_shift_task(db, shift_task_id=shift_task_id)

    if db_shift_task is None:
        raise HTTPException(status_code=404, detail="Shift task not found")

    return db_shift_task


@shift_tasks_router.patch('/{shift_task_id}', response_model=schemas.ShiftTask)
def update_shift_task(shift_task_id: int, shift_task: schemas.ShiftTaskUpdate, db: Session = Depends(database.get_db)):
    db_shift_task = crud.get_shift_task(db, shift_task_id=shift_task_id)

    if db_shift_task is None:
        raise HTTPException(status_code=404, detail="Shift task not found")

    return crud.update_shift_task(db=db, shift_task_id=shift_task_id, shift_task=shift_task)


@shift_tasks_router.get('/', response_model=list[schemas.ShiftTask])
def get_shift_tasks(skip: int = 0,
                    limit: int = 20,
                    db: Session = Depends(database.get_db),
                    shift_tasks_filter: ShiftTaskFilter = FilterDepends(ShiftTaskFilter)):
    shift_tasks = crud.get_shift_tasks(db, skip=skip, limit=limit, shift_tasks_filter=shift_tasks_filter)

    return shift_tasks


@shift_tasks_router.post('/create_products/', response_model=list[schemas.ShiftTaskWithUniqueCode])
def create_products_unique_code(products_unique_codes: list[schemas.ShiftTaskWithUniqueCodeCreate],
                                db: Session = Depends(database.get_db)):
    return services.create_products_unique_code(products_unique_codes=products_unique_codes, db=db)


@shift_tasks_router.patch('/aggregate/', response_model=schemas.ShiftTaskWithUniqueCode)
def aggregate_shift_task(data: schemas.AggregateModel, db: Session = Depends(database.get_db)):
    return services.aggregate_shift_task(data=data, db=db)
