import pandas as pd
from datetime import datetime
from config.db import SessionLocal
from src.credits.models import User, Credit, Dictionary, Plan, Payment


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def import_data_from_csv():
    user_data = pd.read_csv('data/users.csv', delimiter='\t')
    credit_data = pd.read_csv('data/credits.csv', delimiter='\t')
    dictionary_data = pd.read_csv('data/dictionary.csv', delimiter='\t')
    plan_data = pd.read_csv('data/plans.csv', delimiter='\t')
    payment_data = pd.read_csv('data/payments.csv', delimiter='\t')

    db = next(get_db())
    # Користувачі
    for _, row in user_data.iterrows():
        db.add(User(login=row['login'], registration_date=datetime.strptime(row['registration_date'], '%d.%m.%Y')))

    db.commit()
    # Кредити
    for _, row in credit_data.iterrows():
        if db.query(User).filter(User.id == row['user_id']).first():
            db.add(Credit(user_id=row['user_id'],
                          issuance_date=datetime.strptime(row['issuance_date'], '%d.%m.%Y'),
                          return_date=datetime.strptime(row['return_date'], '%d.%m.%Y'),
                          actual_return_date=datetime.strptime(row['actual_return_date'], '%d.%m.%Y') if pd.notna(
                              row['actual_return_date']) else None,
                          body=row['body'],
                          percent=row['percent']))
        else:
            print(f'User ID {row["user_id"]} not found for Credit record')
    db.commit()
    # Словник
    for _, row in dictionary_data.iterrows():
        db.add(Dictionary(name=row['name']))

    db.commit()
    # Плани
    for _, row in plan_data.iterrows():
        if db.query(Dictionary).filter(Dictionary.id == row['category_id']).first():
            db.add(Plan(period=datetime.strptime(row['period'], '%d.%m.%Y'),
                        sum=row['sum'],
                        category_id=row['category_id']))

        else:
            print(f"Category ID {row['category_id']} not found for Plan record")

    db.commit()

    # Платежі
    for _, row in payment_data.iterrows():
        if db.query(Credit).filter(Credit.id == row['credit_id']).first() and db.query(Dictionary).filter(
                Dictionary.id == row['type_id']).first():
            db.add(Payment(sum=row['sum'],
                           payment_date=datetime.strptime(row['payment_date'], '%d.%m.%Y'),
                           credit_id=row['credit_id'],
                           type_id=row['type_id']))
        else:
            print(f"Invalid Credit ID or Type ID for Payment record.")
    db.commit()

    print("Дані успішно імпортовані!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


if __name__ == "__main__":
    import_data_from_csv()
