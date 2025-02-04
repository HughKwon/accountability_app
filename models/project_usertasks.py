from db import db

class ProjectUserTasks(db.Model):
    __tablename__ = "project_usertasks"

    id = db.Column(db.Integer, primary_key=True)
    usertask_id = db.Column(db.Integer, db.ForeignKey("usertasks.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))