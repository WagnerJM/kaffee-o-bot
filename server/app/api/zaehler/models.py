from app.database import BaseMixin, db

class Zaehler(BaseMixin, db.Model):
    __tablename__ = 'zaehler'

    zaehlerID = db.Column(db.Integer, primary_key=True)
    zName = db.Column(db.String)
    wert = db.Column(db.Integer)

    def __init__(self, name ,start_wert):
        self.zName = name
        self.wert = start_wert

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(zName=name).first()

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "wert": self.wert
        }
