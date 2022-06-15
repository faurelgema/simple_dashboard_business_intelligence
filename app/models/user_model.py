from app import db
from datetime import datetime
from werkzeug.security import *
from sqlalchemy.orm import relationship
class Users(db.Model):
    __tablename__ = "user"
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String(230), nullable=False)
    password = db.Column('password', db.String(128), nullable=False)
    role = db.Column('role', db.String(128), nullable=False)
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.utcnow)
    # user_id = relationship("Dataset", backref="user")

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    def getById(id):
        return Users.query.filter_by(id=id).first()