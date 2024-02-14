import datetime

from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app import schemas, models


def create_products_unique_code(products_unique_codes: list[schemas.ShiftTaskWithUniqueCodeCreate], db: Session):
    updated_products_unique_codes = []

    for products_unique_code in products_unique_codes:
        try:
            shift_task = db.query(models.ShiftTask).filter(
                models.ShiftTask.batch_number == products_unique_code.batch_number
            ).filter(
                models.ShiftTask.batch_date == products_unique_code.batch_date
            ).first().id
        except AttributeError:
            continue
        else:
            product = dict(unique_code=products_unique_code.unique_code, shift_task=shift_task)
            updated_products_unique_codes.append(product)

    if not updated_products_unique_codes:
        raise HTTPException(status_code=400, detail="No data for adding")

    stmt = insert(models.ProductUniqueCode).values([unique_code for unique_code in updated_products_unique_codes])
    do_nothing_stmt = stmt.on_conflict_do_nothing(index_elements=[models.ProductUniqueCode.unique_code])

    db.execute(do_nothing_stmt)
    db.commit()
    result = db.scalars(do_nothing_stmt.returning(models.ProductUniqueCode),
                        execution_options={"populate_existing": True})

    return result


def aggregate_shift_task(db: Session, data: schemas.AggregateModel):
    db_shift_task = db.query(models.ShiftTask).filter(models.ShiftTask.id == data.shift_task_id).first()
    db_product_unique_code = db.query(models.ProductUniqueCode).filter(
        models.ProductUniqueCode.unique_code == data.unique_code
    ).first()

    if not db_product_unique_code:
        raise HTTPException(status_code=404, detail="Unique code not found")

    else:
        try:
            shift_task_id = db_shift_task.id
        except AttributeError:
            raise HTTPException(status_code=404, detail="Shift task not found")

        if db_product_unique_code.shift_task != shift_task_id:
            raise HTTPException(status_code=400, detail="Unique code is attached to another batch")

        elif db_product_unique_code.is_aggregated:
            raise HTTPException(status_code=400,
                                detail=f"Unique code already used at {db_product_unique_code.aggregated_at}")

        else:
            db_product_unique_code.is_aggregated = True
            db_product_unique_code.aggregated_at = datetime.datetime.now()
            db.add(db_product_unique_code)
            db.commit()
            db.refresh(db_product_unique_code)

        return db_product_unique_code
