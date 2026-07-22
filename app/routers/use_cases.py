from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import require_admin_key
from app.db import get_db
from app.models import UseCase
from app.schemas import UseCaseCreate, UseCaseResult

router = APIRouter(prefix="/use-cases", tags=["use-cases"])


@router.post("", response_model=UseCaseResult, status_code=201, dependencies=[Depends(require_admin_key)])
def create_use_case(payload: UseCaseCreate, db: Session = Depends(get_db)):
    record = UseCase(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("", response_model=list[UseCaseResult])
def list_use_cases(
    industry: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    complexity: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    # Intentionally open, no auth — this is a shared reference library,
    # every other tool in the toolkit is meant to read from it freely.
    query = db.query(UseCase)
    if industry:
        query = query.filter(UseCase.industry == industry)
    if category:
        query = query.filter(UseCase.category == category)
    if complexity:
        query = query.filter(UseCase.complexity == complexity)
    return query.order_by(UseCase.created_at.desc()).all()


@router.get("/{use_case_id}", response_model=UseCaseResult)
def get_use_case(use_case_id: int, db: Session = Depends(get_db)):
    # Also intentionally open, same reasoning as list_use_cases above.
    record = db.get(UseCase, use_case_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Use case not found")
    return record


@router.delete("/{use_case_id}", status_code=204, dependencies=[Depends(require_admin_key)])
def delete_use_case(use_case_id: int, db: Session = Depends(get_db)):
    record = db.get(UseCase, use_case_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Use case not found")
    db.delete(record)
    db.commit()
