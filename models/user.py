from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    account_created_date = db.Column(db.String(80), nullable=False)
    is_staff = db.Column(db.String(80), nullable=False)

    usertasks = db.relationship("UserTaskModel", back_populates="user", lazy="dynamic")

    projects = db.relationship("ProjectModel", back_populates="users", lazy="dynamic")