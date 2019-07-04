from flask import Blueprint
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request, get_jwt_claims
)
from passlib.apps import custom_app_context as pwd_context
from api.points.point_operation import PointOperation
from api.models import User, Points, StoreInfo, Credit
from api import db


send_user_name = Blueprint('send_user_name', __name__)


@send_user_name.route('/login/getUser', methods=['GET'])
@jwt_required
def send():

    claims = get_jwt_claims()
    username = claims['username']
    return jsonify(username=username), 200
