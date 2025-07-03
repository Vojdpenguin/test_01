from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
import pandas as pd
from io import BytesIO
from src.credits.schema import CreditInfo
from typing import List
from config.db import get_db
from sqlalchemy.orm import Session
from src.credits.models import Credit, Payment, Plan
from datetime import datetime

router = APIRouter()


@router.get("/user_credits/{user_id}", response_model=List[CreditInfo])
def get_user_credits(user_id: int, db: Session = Depends(get_db)):
    credits = db.query(Credit).filter(Credit.user_id == user_id).all()

    if not credits:
        raise HTTPException(status_code=404, detail="Credits not found")

    result = []

    for credit in credits:
        credit_info = CreditInfo(
            credit_date=credit.issuance_date,
            credit_sum=credit.body,
            credit_percent=credit.percent,
            is_closed=credit.actual_return_date is not None,
            return_date=credit.return_date
        )

        if credit.actual_return_date:
            total_payments = db.query(Payment).filter(Payment.credit_id == credit.id).all()
            total_sum = sum([payment.sum for payment in total_payments])
            credit_info.actual_return_date = credit.actual_return_date
            credit_info.total_payments = total_sum
        else:
            overdue_days = (datetime.now().date() - credit.return_date).days
            principal_payments = sum(
                [p.sum for p in db.query(Payment).filter(Payment.credit_id == credit.id, Payment.type_id == 1)])
            interest_payments = sum(
                [p.sum for p in db.query(Payment).filter(Payment.credit_id == credit.id, Payment.type_id == 2)])

            credit_info.overdue_days = overdue_days
            credit_info.principal_payments = principal_payments
            credit_info.interest_payments = interest_payments

        result.append(credit_info)

    return result


@router.post("/plans_insert")
def plans_insert(file: UploadFile = File(), db: Session = Depends(get_db)):
    contents = file.file.read()
    df = pd.read_excel(BytesIO(contents))

    required_columns = ['period', 'category_id', 'sum']
    for column in required_columns:
        if column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing column {column}")

    for index, row in df.iterrows():
        date = row['period']
        category_id = row['category_id']
        amount = row['sum']

        if not isinstance(date, datetime):
            raise HTTPException(status_code=400, detail="Invalid date format")
        if date.day != 1:
            raise HTTPException(status_code=400, detail="Month must be the first day")

        if pd.isnull(amount):
            raise HTTPException(status_code=400, detail="Amount cant be empty")

        existing_plan = db.query(Plan).filter(Plan.period == date, Plan.category_id == category_id).first()
        if existing_plan:
            raise HTTPException(status_code=400, detail="Plan for month already exist")

    for index, row in df.iterrows():
        date = row['period']
        category_id = row['category_id']
        amount = row['sum']

        new_plan = Plan(
            period=date,
            category_id=category_id,
            sum=amount
        )
        db.add(new_plan)

    db.commit()
    return {"message": "plans successfully inserted"}
