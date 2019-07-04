from flask import Blueprint
from flask import Blueprint
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)
from passlib.apps import custom_app_context as pwd_context
from api.models import User, Points, StoreInfo, Credit, find_user, find_user_phone
from api.sign_up.models import PhoneNumber, find_number
from api import db
create_account = Blueprint('create_account', __name__)


@create_account.route('/signup/create_account', methods=['POST'])
@jwt_required
def create_acc():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request

    username = request.json.get('username')
    password = request.json.get('password')
    role = request.json.get('role')
    phone_number = request.json.get('phone_number')

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if not role:
        return jsonify({"msg": "Missing role parameter"}), 400

    if not phone_number:
        return jsonify({"msg": "Missing phone_number parameter"}), 400
    if find_user(username) or find_user_phone(phone_number):
        # conflict
        return jsonify({"msg": "username or number  already taken"}), 409

    number = find_number(phone_number)
    if number != None:
        number_id = number.id
        if number.check_validity(number_id):
            # create

            hashed_password = pwd_context.encrypt(password)
            new_user = User(username=username, password_hash=hashed_password,
                            role=role, phone=phone_number)
            new_credit = Credit(balance=0, precredit=0)
            try:
                db.session.add(new_user)
                db.session.add(new_credit)
                db.session.commit()
                user = db.session.query(User).filter_by(
                    username=username).first()
                user_id = user.id
                return jsonify({"msg": "account_created", "id": user_id}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({"msg": f"error '{e}'"}), 500

        return jsonify({"msg": "phone verification expired"}), 410  # Gone

    return jsonify({"msg": "unverified phone number"}), 400
