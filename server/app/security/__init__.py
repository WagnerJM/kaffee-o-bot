from app.database import BaseMixin, db

class TokenBlacklist(BaseMixin, db.Model):
    __tablename__ = 'tokenBlacklist'

    tokenID = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String)

    def __init__(self, jti):
        self.jti = jti
