from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.config import Config
from flask_jwt_extended import JWTManager

APP_ID = 43256708
COMMISION = .5     # 5 %
MIN_CREDIT = 10  # 10 EGP
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    from api.sign_up.authentication import api_authentication
    from api.sign_up.phone_verification import phone_verification
    from api.sign_up.code_verification import code_verification
    from api.sign_up.new_store import create_store
    from api.sign_up.new_account import create_account
    from api.reset_password.authentication import api_reset_authentication
    from api.reset_password.phone_verification import reset_phone_verification
    from api.reset_password.code_verification import reset_code_verification
    from api.reset_password.reset_password import reset_password
    from api.login.authentication import login_authentication
    from api.points.send_points import send_all_points
    from api.ta7weel.check_eligabilty import check_eligabilty
    from api.ta7weel.ta7weel import transfer
    from api.enquiry.credit_enquiry import credit_info
    from api.enquiry.my_operations import operations_info
    from api.login.get_username import send_user_name

    app.register_blueprint(api_authentication)
    app.register_blueprint(phone_verification)
    app.register_blueprint(code_verification)
    app.register_blueprint(create_store)
    app.register_blueprint(create_account)
    app.register_blueprint(api_reset_authentication)
    app.register_blueprint(reset_phone_verification)
    app.register_blueprint(reset_code_verification)
    app.register_blueprint(reset_password)
    app.register_blueprint(login_authentication)
    app.register_blueprint(send_all_points)
    app.register_blueprint(check_eligabilty)
    app.register_blueprint(transfer)
    app.register_blueprint(credit_info)
    app.register_blueprint(operations_info)
    app.register_blueprint(send_user_name)
    return app
