from flask import Blueprint
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)

from api.sign_up.models import PhoneNumber
from api.sign_up.models import find_code, add_verified_number


code_verification = Blueprint('code_verification', __name__)


@code_verification.route('/signup/verify_code', methods=['POST'])
@jwt_required
def verify_code():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request

    phone_number = request.json.get('phone_number')
    code_number = request.json.get('code_number')
    print(type(code_number))

    if not phone_number:
        return jsonify({"msg": "Missing phone_number parameter"}), 400

    if not code_number:
        return jsonify({"msg": "Missing code_number parameter"}), 400

    code = find_code(code_number, phone_number)
    if code != None:
        isvalid = code.check_validity(code.id)
        if isvalid:
            add_verified_number(phone_number)
            return jsonify({"msg": "valid code"}), 200
        return jsonify({"msg": "code expired"}), 410  # Gone
    return jsonify({"msg": "Bad code"}), 400
