from passlib.apps import custom_app_context as pwd_context
import datetime
from functools import wraps
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask import Blueprint
from api import APP_ID, jwt


APP_USERNAME = 'uncashapp'
APP_PASSWORD_HASH = '$6$rounds=656000$QEBmzPEPqZS5DrgZ$pUh9ze7EpZIP6s1bRwXYSJpS5REsfOX8qfiggUUBFSMMm3EgcBSZTLjJsqSHKHLfJC33FTNQ8HT/xbMoleyDg.'

api_authentication = Blueprint('api_authentication', __name__)


def check_user_credentials(username, password):
    isvalid_password = pwd_context.verify(password, APP_PASSWORD_HASH)
    isvalid_username = (username == APP_USERNAME)
    return (isvalid_password and isvalid_username)


# authentication manangement
@api_authentication.route('/signup/authentication', methods=['POST'])
def authenticate_app():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request

    username = request.json.get('username')
    password = request.json.get('password')
    if not username:
        # Bad request
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        # Bad request
        return jsonify({"msg": "Missing password parameter"}), 400
    # authenticate
    isvalid_credentials = check_user_credentials(username, password)

    if not isvalid_credentials:
        # unauthorized
        return jsonify({"msg": "Bad username or password"}), 401
    expires = datetime.timedelta(hours=1)
    access_token = create_access_token(identity=APP_ID, expires_delta=expires)
    return jsonify(access_token=access_token), 200   # ok
