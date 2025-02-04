from db import db

class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=True, nullable=False)

    # usertask_id = db.Column(db.Integer, db.ForeignKey("usertasks.id"), nullable=True, unique=False)
    # usertask = db.relationship("UserTaskModel", back_populates="task")

    usertasks = db.relationship("UserTaskModel", back_populates="task", lazy="dynamic")
