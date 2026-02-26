from ..config.ext import db

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    card_number = db.Column(db.String(16), unique=True, nullable=False)

    user = db.relationship('User', backref=db.backref('accounts', lazy=True))

    def __repr__(self):
        return f'<Account {self.card_number} - Balance: {self.balance}>'
    
    def put_into_dto(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'card_number': self.card_number
        }
    
    @staticmethod
    def get_from_dto(dto):
        return Account(
            user_id=dto['user_id'],
            balance=dto['balance'],
            card_number=dto['card_number']
        )
    