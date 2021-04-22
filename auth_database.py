from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Authorized(db.Model):
    __tablename__ = 'Authorized'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)