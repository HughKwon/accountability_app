from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from db import db
from models import UserModel

import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    jwt_required,
    create_refresh_token,
    get_jwt_identity
)
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token
from schemas import UserSchema, UserTaskSchema, UserUpdateSchema, UserLogInOutSchma
from blocklist import BLOCKLIST



blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort (409, message="A user with that username already exists.")

        user = UserModel(
            username = user_data["username"],
            email = user_data["email"],
            password = pbkdf2_sha256.hash(user_data["password"]),
            is_staff = user_data["is_staff"],
            account_created_date = user_data["account_created_date"],
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A user with that username already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user.")

        return {"message": "User created successfully"}, 201


@blp.route("/user/<string:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return(user)

    @jwt_required(fresh=True)
    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserUpdateSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id)
        user.username = user_data["username"]
        user.password = pbkdf2_sha256.hash(user_data["password"])
        user.is_staff = user_data["is_staff"]
        user.email = user_data["email"]

        db.session.add(user)
        db.session.commit()

        return user

    @jwt_required(fresh=True)
    def delete(self, user_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin priviledge required.")
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLogInOutSchma)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
            ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refersh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200




