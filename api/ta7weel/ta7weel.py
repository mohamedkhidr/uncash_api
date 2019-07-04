from flask import Blueprint
from flask import Flask, jsonify, request
from datetime import datetime
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)
from passlib.apps import custom_app_context as pwd_context
from api.points.point_operation import PointOperation
from api.models import (User, Points, StoreInfo, Credit, find_user,
                        get_user_id, is_covered, withdrawal, deposit,
                        new_operation, get_user_name, get_operation_id, OurCommissions, commission_withdrawal, commission_deposit)
from api import db, COMMISION, MIN_CREDIT


transfer = Blueprint('transfer', __name__)


@transfer.route('/feature/ta7weel/transfer', methods=['Post'])
@jwt_required
def go():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request
    claims = get_jwt_claims()

    sender_id = claims['user_id']
    print(sender_id)

    receiver_id = request.json.get('receiver_id')
    amount = request.json.get('amount')

    provider_id = request.json.get('provider_id')
    provider_commission = request.json.get('provider_commission')

    if sender_id == 0:
        # Bad request
        return jsonify({"msg": "Missing sender_id parameter"}), 400
    if receiver_id == 0:
        # Bad request
        return jsonify({"msg": "Missing receiver_id parameter"}), 400

    if amount == 0:
        # Bad request
        return jsonify({"msg": "Missing amount parameter"}), 400

    if provider_id < 0:
        # Bad request
        return jsonify({"msg": "Missing provider_id parameter"}), 400
    if provider_commission == 0:
        # Bad request
        return jsonify({"msg": "Missing provider_commission parameter"}), 400

    sender_username = get_user_name(sender_id)
    print(sender_username)
    print(receiver_id)
    receiver_username = get_user_name(receiver_id)
    print(receiver_username)

# amount : withdrawal from sender and deposit in the receiver
    is_withdrawal_done = withdrawal(sender_id, amount)
    is_deposit_done = deposit(receiver_id, amount)

    if is_withdrawal_done and is_deposit_done:
        if provider_id == sender_id:
            # provider_commission : withdrawal from client and deposit in the provider

            is_provider_commission_withdrawal_done = commission_withdrawal(
                receiver_id, provider_commission)
            is_provider_commission_deposit_done = commission_deposit(
                sender_id, provider_commission)

            if is_provider_commission_withdrawal_done and is_provider_commission_deposit_done:
                # log

                if commission_withdrawal(receiver_id, provider_commission):
                    time = datetime.now()
                    total = int(provider_commission * 2 + amount)
                    new_operation(sender_username, receiver_username, sender_username, amount,
                                  time, total, provider_commission)

                # add our commission

                operation_id = get_operation_id(time)
                our_commission = OurCommissions(
                    operation_id=operation_id, amount=provider_commission, client_id=receiver_id)
                try:
                    db.session.add(our_commission)
                    db.session.commit()
                    return jsonify({"msg": "operation done ", "id": operation_id}), 200
                except Exception as e:
                    return jsonify({"msg": f"internal error '{e}'"}), 500

        elif provider_id == receiver_id:
            # provier_commission : withdrawal from client and deposit in the provider

            is_provider_commission_withdrawal_done = commission_withdrawal(
                sender_id, provider_commission)
            is_provider_commission_deposit_done = commission_deposit(
                receiver_id, provider_commission)

            if is_provider_commission_withdrawal_done and is_provider_commission_deposit_done:
                if commission_withdrawal(sender_id, provider_commission):
                    # log

                    time = datetime.now()
                    total = int(provider_commission * 2 + amount)
                    new_operation(sender_username, receiver_username, receiver_username, amount,
                                  time, total, provider_commission)
                else:
                    return jsonify({"msg": "internal error"}), 500

                # add our commission
                operation_id = get_operation_id(time)
                our_commission = OurCommissions(
                    operation_id=operation_id, amount=provider_commission, client_id=sender_id)
                try:
                    db.session.add(our_commission)
                    db.session.commit()
                    return jsonify({"msg": "operation done ", "id": operation_id}), 200
                except Exception as e:
                    db.session.rollback()
                    return jsonify({"msg": f"internal error '{e}'"}), 500

        elif provider_id == 0:
            print(3333)
            is_our_commission_withdrawal_done = commission_withdrawal(
                sender_id, provider_commission)
            if is_our_commission_withdrawal_done:
                time = datetime.now()
                total = int(provider_commission + amount)
                new_operation(sender_username, receiver_username, 0, amount,
                              time, total, provider_commission)

                # add out commission
                operation_id = get_operation_id(time)
                our_commission = OurCommissions(
                    operation_id=operation_id, amount=provider_commission, client_id=sender_id)
                try:
                    db.session.add(our_commission)
                    db.session.commit()
                    return jsonify({"msg": "operation done ", "id": operation_id}), 200
                except Exception as e:
                    db.session.rollback()
                    return jsonify({"msg": f"internal error '{e}'"}), 500
