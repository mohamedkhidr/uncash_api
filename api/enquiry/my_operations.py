from flask import Blueprint
from flask import Flask, jsonify, request
from datetime import datetime
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)
from passlib.apps import custom_app_context as pwd_context
from api.points.point_operation import PointOperation
from api.models import Credit, Operation, get_user_name
from api import db, COMMISION, MIN_CREDIT


operations_info = Blueprint('operations_info', __name__)


@operations_info.route('/feature/enquiry/operations_info', methods=['GET'])
@jwt_required
def get_operations():

    claims = get_jwt_claims()
    user_id = claims['user_id']

    username = get_user_name(user_id)

    all_operations = []

    operations = db.session.query(Operation).filter_by(
        source_username=username).all()

    operations_ = db.session.query(Operation).filter_by(
        destination_username=username).all()
    if operations != None and operations_ != None:
        for operation in operations:
            all_operations.append(operation.serialize)

        for operation_ in operations_:
            all_operations.append(operation_.serialize)

        return jsonify(all_operations), 200
    elif operations != None and not operations_ != None:
        for operation in operations:
            all_operations.append(operation.serialize)

        return jsonify(all_operations), 200

    elif not operations != None and operations_ != None:
        print("rrrr")
        for operation_ in operations_:
            all_operations.append(operation_.serialize)

        return jsonify(all_operations[0]), 200
    else:
        return jsonify({"msg": "no operations found"}), 404
