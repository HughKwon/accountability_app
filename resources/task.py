import uuid
import logging
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from models import TaskModel, UserTaskModel
from schemas import TaskSchema
from db import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blp = Blueprint("tasks", __name__, description="Operations on tasks")

@blp.route("/task")
class TaskCreate(MethodView):
    @jwt_required()
    @blp.arguments(TaskSchema)
    def post(self, task_data):
        task = TaskModel(**task_data)

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="An error occurred while inserting the task.")


        return {"message": "Task created successfully"}, 201

@blp.route("/task/<string:task_id>")
class Task(MethodView):
    @jwt_required()
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return(task)

    @jwt_required(fresh=True)
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted."}, 200


@blp.route("/task/<string:task_id>/usertask/<int:usertask_id>")
class TaskUserTaskLink(MethodView):
    @jwt_required()
    @blp.response(200, TaskSchema)
    def post(self, task_id, usertask_id):
        task = TaskModel.query.get_or_404(task_id)
        usertask = UserTaskModel.query.get_or_404(usertask_id)

        task.usertasks.add(usertask)

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while linking the usertask to task")

        return task

    @jwt_required(fresh=True)
    def delete(self, task_id, usertask_id):
        task = TaskModel.query.get_or_404(task_id)
        usertask = UserTaskModel.query.get_or_404(usertask_id)

        task.usertask.remove(usertask)

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred while un-linking the usertask from the task")

        return {"message": "usertask successfully removed from the task."}, 200
