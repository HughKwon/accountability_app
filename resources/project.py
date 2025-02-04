import uuid
from flask import request
from db import db
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from models import UserModel, ProjectModel, UserTaskModel
from schemas import PlainProjectSchema, ProjectSchema, ProjectUserTaskSchema

blp = Blueprint("projects", __name__, description="Operations on projects")

@blp.route("/user/<int:user_id>/project")
class ProjectList(MethodView):
    @jwt_required()
    @blp.arguments(PlainProjectSchema)
    @blp.response(200, ProjectSchema)
    def post(self, project_data, user_id):
        user = UserModel.query.get_or_404(user_id)
        project = ProjectModel(**project_data, user_id=user_id)

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
            # abort(500, message="An error occurred while creating the project.")

        return project
    @jwt_required()
    @blp.response(200, ProjectSchema(many=True))
    def get(self, user_id):
        project = ProjectModel.query.filter_by(user_id=user_id).all()

        return project

@blp.route("/user/<int:user_id>/project/<int:project_id>")
class Project(MethodView):
    @jwt_required()
    @blp.response(200, ProjectSchema)
    def get(self,user_id, project_id):
        project = ProjectModel.query.filter_by(
            user_id = user_id,
            id = project_id
        ).first_or_404()

        return project

    @jwt_required()
    def delete(self, user_id, project_id):
        project = ProjectModel.query.filter_by(
            user_id = user_id,
            project_id = project_id
        ).first_or_404

        db.session.delete(project)
        db.session.commit()

        return {"message": "Project successfully deleted."}


@blp.route("/project/<int:project_id>/usertask/<int:usertask_id>")
class ProjectUserTaskLink(MethodView):
    @blp.response(201, ProjectUserTaskSchema)
    def post(self, project_id, usertask_id):
        project = ProjectModel.query.get_or_404(project_id)
        usertask = UserTaskModel.query.get_or_404(usertask_id)

        project.usertasks.append(usertask)

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while linking the usertask to the project.")

        return project
    @jwt_required()
    def delete(self, project_id, usertask_id):
        project = ProjectModel.query.get_or_404(project_id)
        usertask = UserTaskModel.query.get_or_404(usertask_id)

        project.usertask.delete(usertask)

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the usertask from the project.")

        return {"message": "UserTask removed from project."}, 200