from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreditInfo(BaseModel):
    credit_date: datetime # Дата видачі кредиту
    credit_sum: float # Сума кредиту
    credit_percent: float # Нараховані відсотки
    is_closed: bool # Закритий чи відкритий кредит
    return_date: datetime # Планова дата повернення
    actual_return_date: datetime = None # Дата повернення
    total_payments: float = 0 # Загальна сума виплат
    overdue_days: int = 0 # Дні прострочення після дати повернення
    principal_payments: float = 0 # Сума сплачена по тілу кредиту
    interest_payments: float = 0 # Сума зплачена по відсоткахх

    class Config:
        orm_mode = True