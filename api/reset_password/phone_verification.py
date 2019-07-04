
from functools import wraps
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)
from flask import Blueprint
from api import APP_ID, jwt, db
from api.reset_password.models import CodesReset, generate_code
from api.models import User


reset_phone_verification = Blueprint('reset_phone_verification', __name__)


@reset_phone_verification.route('/reset_password/verify_phone', methods=['POST'])
@jwt_required
def verify_phone():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request

    phone_number = request.json.get('phone_number')

    if not phone_number:
        return jsonify({"msg": "Missing phone_number parameter"}), 400
    user = db.session.query(User).filter_by(phone=phone_number).first()
    if user != None:
        new_code = generate_code(phone_number)
        new_code.send_code_number()
        return jsonify({"msg": "code sent "}), 200
    return jsonify({"msg": "no account with this phone number "}), 404
