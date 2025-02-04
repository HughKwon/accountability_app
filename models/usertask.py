from db import db

class UserTaskModel(db.Model):
    __tablename__ = "usertasks"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(80), unique=True, nullable=False)
    occurrence_type = db.Column(db.String(80), nullable=False)
    scoring = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    start_datetime = db.Column(db.String(80), nullable=False)
    due_datetime = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    user = db.relationship("UserModel", back_populates="usertasks")

    # task = db.relationship("TaskModel", back_populates="usertask", lazy="dynamic")

    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), unique=False, nullable=True)
    task = db.relationship("TaskModel", back_populates="usertasks")

    projects = db.relationship("ProjectModel", back_populates="usertasks", secondary="project_usertasks")