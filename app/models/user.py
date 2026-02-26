from ..config.ext import db

class User(db.Model):
    __timetable__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    tax_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(240), nullable=False)

    def __repr__(self):
        return f'<User {self.name} {self.surname}>'
    
    def put_into_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'tax_id': self.tax_id,
            'surname': self.surname,
            'email': self.email
        }
    
    @staticmethod
    def get_from_dto(dto):
        return User(
            name=dto['name'],
            surname=dto['surname'],
            tax_id=dto['tax_id'],
            email=dto['email'],
            password=dto['password']
        )