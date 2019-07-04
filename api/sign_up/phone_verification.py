
from functools import wraps
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)
from flask import Blueprint
from api import APP_ID, jwt
from api.sign_up.models import Codes, generate_code
from api.models import User, find_user_phone


phone_verification = Blueprint('phone_verification', __name__)


@phone_verification.route('/signup/verify_phone', methods=['POST'])
def verify_phone():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request

    phone_number = request.json.get('phone_number')

    if not phone_number:
        return jsonify({"msg": "Missing phone_number parameter"}), 400
    if find_user_phone(phone_number):
        return jsonify({"msg": "phone is already used "}), 409  # conflict

    new_code = generate_code(phone_number)
    new_code.send_code_number()
    return jsonify({"msg": "code sent "}), 200
