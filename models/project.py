from db import db

class ProjectModel(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(80))
    description = db.Column(db.String(80), unique=True, nullable=False)

    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), unique=False, nullable=False)
    users = db.relationship("UserModel", back_populates="projects")

    usertasks = db.relationship("UserTaskModel", back_populates="projects", secondary="project_usertasks")