import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from models import UserTaskModel, UserModel, ProjectModel
from schemas import UserTaskSchema, PlainUserTaskSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
import json

blp = Blueprint("UserTasks", __name__, description="Operations on user tasks")


@blp.route("/user/<int:user_id>/usertask")
class UserTaskList(MethodView):
    @jwt_required()
    @blp.arguments(PlainUserTaskSchema)
    def post(self, usertask_data, user_id):
        # usertask = UserTaskModel({"user_id": user_id}| usertask_data)
        usertask_data["user_id"] = user_id
        usertask = UserTaskModel(**usertask_data)

        try:
            db.session.add(usertask)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, "Error while inserting UserTask")

        return {"message": "UserTask created successfully"}, 201

    @jwt_required()
    @blp.response(200, UserTaskSchema(many=True))
    def get(self, user_id):

        user = UserModel.query.get_or_404(user_id)
        return UserTaskModel.query.filter_by(user_id=user_id).all()

    @jwt_required()
    def delete(self, usertask_id):
        usertask = UserTaskModel.query.get_or_404(usertask_id)
        db.session.delete(usertask)
        db.session.commit()
        return {"message": "UserTask deleted."}

@blp.route("/user/<int:user_id>/usertask/<int:usertask_id>")
class UserTask(MethodView):
    @jwt_required()
    @blp.response(200, UserTaskSchema)
    def get(self, user_id, usertask_id):
        usertask = UserTaskModel.query.filter_by(
            id=usertask_id,
            user_id=user_id).first_or_404()
        # usertask = UserTaskModel.query.all()
        return usertask

    @jwt_required()
    def delete(self, user_id, usertask_id):
        usertask = UserTaskModel.query.filter_by(
            id=usertask_id,
            user_id=user_id
        ).first_or_404()
        db.session.delete(usertask)
        db.session.commit()
        return {"message": "UsterTask deleted successfully"}, 200

