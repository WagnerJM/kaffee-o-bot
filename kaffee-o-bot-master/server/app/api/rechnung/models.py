from app.database import BaseMixin, db
from app.api.user.models import User

class Rechnung(BaseMixin, db.Model):
    __tablename__ = 'rechnungen'

    rechnungID = db.Column(db.Integer, primary_key=True)
    rechnungsnr = db.Column(db.Integer)
    rechnungsBetrag = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))
    bezahlt = db.Column(db.Boolean, default=False)

    def __init__(self, rechnungsnr, rechnungsBetrag, bezahlt):
        self.rechnungsnr = rechnungsnr
        self.rechnungsBetrag = rechnungsBetrag
        self.bezahlt = bezahlt

    @classmethod
    def get_by_RechnungsNr(cls, nr):
        return cls.query.filter_by(rechnungsnr=nr).first()

    def json(self):
        return {
            "id": str(self.id),
            "rechnungsnr": self.rechnungsnr,
            "rechnungsBetrag": self.rechnungsBetrag,
            "bezahlt": self.bezahlt
        }
