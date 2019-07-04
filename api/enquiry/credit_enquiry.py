from flask import Blueprint
from flask import Flask, jsonify, request
from datetime import datetime
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)
from passlib.apps import custom_app_context as pwd_context
from api.points.point_operation import PointOperation
from api.models import Credit
from api import db, COMMISION, MIN_CREDIT


credit_info = Blueprint('credit_info', __name__)


@credit_info.route('/feature/enquiry/credit', methods=['GET'])
@jwt_required
def get_credit_info():

    claims = get_jwt_claims()

    user_id = claims['user_id']

    user_credit = db.session.query(Credit).filter_by(id=user_id).first()
    balance = user_credit.balance
    prebalance = user_credit.precredit

    return jsonify({"balance": balance, "prebalance": prebalance}), 200
