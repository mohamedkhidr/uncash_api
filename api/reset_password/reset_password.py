from flask import Blueprint
from flask import Blueprint
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)
from passlib.apps import custom_app_context as pwd_context
from api.models import User, Points, StoreInfo, Credit, find_user, find_user_phone
from api.reset_password.models import PhoneNumberReset, find_number
from api import db
reset_password = Blueprint('reset_password', __name__)


@reset_password.route('/reset_password/reset', methods=['POST'])
@jwt_required
def reset():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request

    password = request.json.get('password')
    phone_number = request.json.get('phone_number')

    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if not phone_number:
        return jsonify({"msg": "Missing phone_number parameter"}), 400

    number = find_number(phone_number)
    if number != None:
        number_id = number.id
        if number.check_validity(number_id):
            # update
            user = db.session.query(User).filter_by(phone=phone_number).first()
            old_hashed_password = user.password_hash
            isthesame = pwd_context.verify(password, old_hashed_password)
            new_hashed_password = pwd_context.encrypt(password)
            if isthesame:
                return jsonify({"msg": "not valid password"}), 409  # conflict
            user.password_hash = new_hashed_password
            try:
                db.session.add(user)
                db.session.commit()
                user = db.session.query(User).filter_by(
                    phone=phone_number).first()
                user_id = user.id
                return jsonify({"msg": "password updated", "id": user_id}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({"msg": f"error '{e}'"}), 500

        return jsonify({"msg": "phone verification expired"}), 410  # Gone

    return jsonify({"msg": "unverified phone number"}), 400
