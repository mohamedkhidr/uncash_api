from flask import Blueprint
from math import ceil
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)
from passlib.apps import custom_app_context as pwd_context
from api.points.point_operation import PointOperation
from api.models import User, Points, StoreInfo, Credit, find_user, get_user_id, is_covered, is_provider, get_user_role
from api import db, COMMISION, MIN_CREDIT


check_eligabilty = Blueprint('check_eligabilty', __name__)


@check_eligabilty.route('/feature/ta7weel/check_eligabilty', methods=['Post'])
@jwt_required
def check():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request
    claims = get_jwt_claims()
    sender_username = claims['username']
    receiver_username = request.json.get('receiver_username')
    amount = request.json.get('amount')

    if not sender_username:
        # Bad request
        return jsonify({"msg": "Missing sender_username parameter"}), 400
    if not receiver_username:
        # Bad request
        return jsonify({"msg": "Missing receiver_username parameter"}), 400

    if not amount:
        # Bad request
        return jsonify({"msg": "Missing amount parameter"}), 400

    if find_user(receiver_username):
        sender_id = get_user_id(sender_username)
        receiver_id = get_user_id(receiver_username)

        sender_role = get_user_role(sender_username)
        receiver_role = get_user_role(receiver_username)

        if sender_role != receiver_role:
            provider_commission = int(ceil((amount * COMMISION) / 100))
            operation_commission = provider_commission
            min_current_credit = MIN_CREDIT + \
                operation_commission + provider_commission + amount
            total = operation_commission + provider_commission + amount

            if is_covered(sender_id, min_current_credit):
                print('done')
                if is_provider(sender_id) and not is_provider(receiver_id):
                    operation_info = {
                        's_id': sender_id,
                        'd_id': receiver_id,
                        'amount': amount,
                        'provider_id': sender_id,
                        'commission': operation_commission,
                        'total': total
                    }
                    return jsonify(operation_info), 200
                elif not is_provider(sender_id) and is_provider(receiver_id):

                    operation_info = {
                        's_id': sender_id,
                        'd_id': receiver_id,
                        'amount': amount,
                        'provider_id': receiver_id,
                        'commission': operation_commission,
                        'total': total
                    }
                    return jsonify(operation_info), 200
            return jsonify({"msg": "insufficient credit "}), 401

        else:
            operation_commission = int(ceil((amount * COMMISION) / 100))
            min_current_credit = MIN_CREDIT + operation_commission + amount
            total = operation_commission + amount
            if is_covered(sender_id, min_current_credit):
                operation_info = {
                    's_id': sender_id,
                    'd_id': receiver_id,
                    'amount': amount,
                    'provider_id': 0,
                    'commission': operation_commission,
                    'total': total
                }
                return jsonify(operation_info), 200
            return jsonify({"msg": "insufficient credit "}), 401

    return jsonify({"msg": "receiver username not found"}), 404
