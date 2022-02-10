from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
    get_jwt,
    unset_jwt_cookies,
    jwt_required,
    current_user,
)

from .models import User
from .schema import UserSchema

from . import db

bp = Blueprint("auth", __name__, url_prefix="/auth")
one_user_schema = UserSchema()
multi_user_schema = UserSchema(many=True)


# GET endpoints


@bp.route("/check", methods=["GET"])
@jwt_required(optional=True)
def check_for_logged_in_user():
    if current_user != None:
        return jsonify(one_user_schema.dump(current_user))
    return jsonify({})


# POST endpoints


@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if User.query.filter_by(username=username).first() == None:
        new_user = User(username=username, password=User.hash_password(password))
        db.session.add(new_user)
        db.session.commit()
        response = jsonify(one_user_schema.dump(new_user))
        access_token = create_access_token(identity=username)
        set_access_cookies(response, access_token)
        return response
    return jsonify("User already exists"), 401


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user_query = User.query.filter_by(username=username).first()
    if user_query == None:
        return jsonify("Invalid username/password"), 401
    if not user_query.check_password(password):
        return jsonify("Invalid username/password"), 401
    response = jsonify(one_user_schema.dump(user_query))
    access_token = create_access_token(identity=username)
    set_access_cookies(response, access_token)
    return response


# DELETE endpoints


@bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200
