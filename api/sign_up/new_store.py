from flask import Blueprint
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request
)
from passlib.apps import custom_app_context as pwd_context
from api.models import User, Points, StoreInfo, Credit, find_user, find_user_phone, find_store
from api.sign_up.models import PhoneNumber, find_number
from api import db

create_store = Blueprint('create_store', __name__)


@create_store.route('/signup/create_store', methods=['POST'])
@jwt_required
def create_account():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400  # Bad request

    username = request.json.get('username')
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    store_name = request.json.get('store_name')
    store_phone = request.json.get('store_phone')

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    if not latitude:
        return jsonify({"msg": "Missing latitude parameter"}), 400
    if not longitude:
        return jsonify({"msg": "Missing longitude parameter"}), 400
    if not store_name:
        return jsonify({"msg": "Missing store_name parameter"}), 400
    if not store_phone:
        return jsonify({"msg": "Missing store_phone parameter"}), 400
    # create
    user = db.session.query(User).filter_by(username=username).first()
    if not user == None:
        user_id = user.id
    else:
        return jsonify({"msg": "username not found "}), 404

    if not find_store(user_id):
        if user.role == 'provider':
            new_point = Points(id=user_id, latitude=latitude,
                               longitude=longitude)
            new_store = StoreInfo(
                id=user_id, name=store_name,  phone=store_phone)
        try:
            db.session.add(new_point)
            db.session.add(new_store)
            db.session.commit()
            return jsonify({"msg": "store_created", "id": user_id}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": f"error '{e}'"}), 500
            # Forbidden
        return jsonify({"msg": "action not allowed for this user"}), 403
    return jsonify({"msg": "user already have a store"}), 409  # conflict
