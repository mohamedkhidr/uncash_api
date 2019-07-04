from flask import Blueprint
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, verify_jwt_in_request, get_jwt_claims
)
from passlib.apps import custom_app_context as pwd_context
from api.points.point_operation import PointOperation
from api.models import User, Points, StoreInfo, Credit
from api import db


send_all_points = Blueprint('send_all_points', __name__)


def serialize(store,  point, credit):
    return {
        'balance': credit.balance,
        'store_name': store.name,
        'store_phone': store.phone,
        'latitude': point.latitude,
        'longitude': point.longitude,
    }


@send_all_points.route('/feature/getPoints', methods=['GET'])
@jwt_required
def send_points():

    all_points = []
    try:
        points = db.session.query(Points).all()
        stores = db.session.query(StoreInfo).all()
        credits = db.session.query(Credit).all()

        claims = get_jwt_claims()
        print(claims['user_id'], claims['username'])

        for store in stores:
            for point in points:
                for credit in credits:
                    if(store.id == point.id):
                        if(store.id == credit.id):
                            all_points.append(serialize(store, point, credit))
        return jsonify(all_points), 200
    except Exception as e:

        return jsonify({"msg": f"'{e}'"}), 500
