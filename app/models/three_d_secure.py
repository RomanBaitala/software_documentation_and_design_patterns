from ..config.ext import db

class ThreeDSecure(db.Model):
    __tablename__ = 'three_d_secure'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    verification_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    transaction = db.relationship('Transaction', backref=db.backref('three_d_secure', uselist=False))

    def __repr__(self):
        return f'<ThreeDSecure {self.id} - Status: {self.status}>'
    
    def put_into_dto(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'verification_code': self.verification_code,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def get_from_dto(dto):
        return ThreeDSecure(
            transaction_id=dto['transaction_id'],
            status=dto['status'],
            verification_code=dto['verification_code'],
            created_at=dto['created_at']
        )