from ..config.ext import db

class BankSystem(db.Model):
    __tablename__ = 'bank_system'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mfo = db.Column(db.String(10), unique=True, nullable=False)
    swift_code = db.Column(db.String(11), unique=True, nullable=False)

    def __repr__(self):
        return f'<BankSystem {self.name}>'
    
    def put_into_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'mfo': self.mfo,
            'swift_code': self.swift_code
        }
    
    @staticmethod
    def get_from_dto(dto):
        return BankSystem(
            name=dto['name'],
            mfo=dto['mfo'],
            swift_code=dto['swift_code']
        )