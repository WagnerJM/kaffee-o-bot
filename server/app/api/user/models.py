import bcrypt
from datetime import datetime
from app.database import BaseMixin, db



class User(BaseMixin, db.Model):

    __tablename__ = 'users'

    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    _password = db.Column(db.Binary(60))

    vorname = db.Column(db.String)
    nachname = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    user_key = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    coffee_count = db.Column(db.Integer, default=0)

    coffee_hist = db.relationship('CoffeeHistory', backref='users', lazy=True)
    rechnungen = db.relationship('Rechnung', backref='users', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = self._hash_pw(password).encode('utf-8')
        self.email = self.email


    def _hash_pw(self, password):
        return bcrypt.hash_pw(password, bcrypt.gensalt(12))

    def check_pw(self, password, hashed_pw):
        return bcrypt.check_pw(password, hashed_pw)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "vorname": self.vorname,
            "nachname": self.nachname,
            "email": self.email,
            "user_key": self.user_key,
            "is_admin": self.is_admin,
            "coffee_count": self.coffee_count,

        }



class CoffeeHistory(BaseMixin, db.Model):
    __tablename__ = 'coffeeHistory'

    coffeeHistID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    coffee_count = db.Column(db.Integer)
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))

    def __init__(self, coffee_count, amount):
        self.coffee_count = coffee_count
        self.amount = amount

    def json(self):
        return {
            "id": str(self.id),
            "date": self.date.strftime('%a, %d, %B, %Y'),
            "coffee_count": self.coffee_count,
            "amount": self.amount
        }
