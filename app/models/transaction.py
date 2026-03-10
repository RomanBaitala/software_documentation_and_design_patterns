from ..config.ext import db
from datetime import datetime, timezone

class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    sender_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    receiver_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'transaction',
        'polymorphic_on': type
    }

    sender_account = db.relationship('Account', foreign_keys=[sender_account_id], backref=db.backref('sent_transactions', lazy=True))

    def __repr__(self):
        return f'<Transaction {self.id} - Amount: {self.amount} from Account {self.sender_account_id} to Account {self.receiver_account_id}>'
    
    def put_into_dto(self):
        return {
            'id': self.id,
            'type': self.type,
            'sender_account_id': self.sender_account_id,
            'receiver_account_id': self.receiver_account_id,
            'amount': self.amount,
            'timestamp': self.timestamp.isoformat()
        }
    
    @staticmethod
    def get_from_dto(dto):
        t_type = dto.get('type')
        
        if t_type == 'payment':
            return Payment(
                sender_account_id=dto['sender_account_id'],
                receiver_account_id=dto['receiver_account_id'],
                amount=dto['amount'],
                timestamp=dto['timestamp'],

                merchant_name=dto.get('merchant_name'),
                category=dto.get('category'),
                is_taxable=dto.get('is_taxable', False)
            )
        elif t_type == 'transfer':
            return Transfer(
                sender_account_id=dto['sender_account_id'],
                receiver_account_id=dto['receiver_account_id'],
                amount=dto['amount'],
                timestamp=dto['timestamp']
            )
        
        return Transaction(
            sender_account_id=dto['sender_account_id'],
            receiver_account_id=dto['receiver_account_id'],
            amount=dto['amount'],
            timestamp=dto['timestamp']
        )
    

class Transfer(Transaction):
    __mapper_args__ = {
        'polymorphic_identity': 'transfer',
    }
    
    def __repr__(self):
        return f'<Transfer {self.id} - Amount: {self.amount} from Account {self.sender_account_id} to Account {self.receiver_account_id}>'
    

class Payment(Transaction):
    merchant_name = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True) 
    is_taxable = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'payment',
    }
    
    def __repr__(self):
        return f'<Payment {self.id} - Amount: {self.amount} from Account {self.sender_account_id} to Account {self.receiver_account_id}>'
    
    def put_into_dto(self):
        dto = super().put_into_dto()
        dto.update({
            'merchant_name': self.merchant_name,
            'category': self.category,
            'is_taxable': self.is_taxable
        })
        return dto
    
