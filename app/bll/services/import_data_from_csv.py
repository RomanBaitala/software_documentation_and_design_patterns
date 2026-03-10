from app.config.ext import db
from app.models.user import User 
from app.models.account import Account
from app.models.transaction import Payment, Transfer

class DataImportService:
    def __init__(self, user_repo, account_repo, transaction_repo, csv_reader):
        self.user_repo = user_repo
        self.account_repo = account_repo
        self.tx_repo = transaction_repo
        self.csv_reader = csv_reader

    def import_all_data(self):
        rows = self.csv_reader.read_all()
        if not rows: return

        print(f"Початок імпорту {len(rows)} рядків...")
        user_cache = {} 

        try:
            for row in rows:
                email = row['user_email']
                
                if email not in user_cache:
                    existing_user = self.user_repo.get_by_email(email)
                    if existing_user:
                        user_cache[email] = existing_user
                    else:
                        new_user = User(
                            name=row['user_name'],
                            email=email,
                            password=row['user_password'],
                            surname=row['user_surname'],
                            tax_id=row['user_tax_id']
                        )
                        self.user_repo.create(new_user)
                        user_cache[email] = new_user
                
                current_user = user_cache[email]

                account = Account(
                    balance=float(row['acc_balance']),
                    card_number=row['acc_card_number'],
                    user=current_user 
                )
                self.account_repo.create(account)
                db.session.flush()

                tx_type = row.get('tx_type')
                amount = float(row['tx_amount']) if row.get('tx_amount') else 0

                if tx_type == 'payment':
                    transaction = Payment(
                        amount=amount,
                        merchant_name=row.get('tx_merchant_name'),
                        category=row.get('tx_category'),
                        sender_account_id=account.id, 
                        receiver_account_id=account.id
                    )
                    self.tx_repo.create(transaction)
                
                elif tx_type == 'transfer':
                    transaction = Transfer(
                        amount=amount,
                        sender_account_id=account.id,
                        receiver_account_id=account.id
                    )
                    self.tx_repo.create(transaction)

            db.session.commit()
            print(f"Імпорт завершено успішно!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Критична помилка: {e}")