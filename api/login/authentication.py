from passlib.apps import custom_app_context as pwd_context
import datetime
from functools import wraps
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask import Blueprint
from api import APP_ID, jwt, db
from api.models import User


login_authentication = Blueprint('login_authentication', __name__)
username = ""


def check_user_credentials(username, password):
    isvalid_password = pwd_context.verify(password, APP_PASSWORD_HASH)
    isvalid_username = (username == APP_USERNAME)
    return (isvalid_password and isvalid_username)


# authentication manangement
@login_authentication.route('/login/authentication', methods=['POST'])
def authenticate_app():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request

    phone_number = request.json.get('phone_number')
    password = request.json.get('password')
    app_id = request.json.get('app_id')
    if not phone_number:
        # Bad request
        return jsonify({"msg": "Missing phone_number parameter"}), 400
    if not password:
        # Bad request
        return jsonify({"msg": "Missing password parameter"}), 400

    if not app_id:
        # Bad request
        return jsonify({"msg": "Missing app_id parameter"}), 400
    # authenticate
    user = db.session.query(User).filter_by(phone=phone_number).first()
    if user != None:
        isvalid_password = pwd_context.verify(password, user.password_hash)
        isvalid_app_id = APP_ID == app_id
        if isvalid_password:
            if isvalid_app_id:
                expires = datetime.timedelta(hours=1)
                access_token = create_access_token(
                    identity=user.id, expires_delta=expires)
                username = user.username
                print(username)
                return jsonify(access_token=access_token), 200
            return jsonify({"msg": "Bad app_id "}), 401
        return jsonify({"msg": "Bad  password"}), 401
    return jsonify({"msg": "Bad phone_number "}), 401


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user_id = identity
    user = db.session.query(User).filter_by(id=user_id).first()
    if user != None:
        username = user.username
        return {
            'role': 'user',
            'user_id': user_id,
            'username': username
        }
