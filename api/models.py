from api import db
from datetime import datetime


class Points(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(10), nullable=False)
    longitude = db.Column(db.String(10), nullable=False)

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
        }


# store info table that have information about each store that provide uncash

class StoreInfo(db.Model):
    __tablename__ = 'storeinfo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
        }


class OurCommissions(db.Model):
    __tablename__ = 'commissions'
    id = db.Column(db.Integer, primary_key=True)
    operation_id = db.Column(db.Integer, unique=True)
    amount = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)


class Credit(db.Model):
    __tablename__ = 'credit'
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)
    precredit = db.Column(db.Integer, nullable=False)

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'balance': self.balance,
        }


def withdrawal(account_id, amount):
    try:
        acc = db.session.query(Credit).filter_by(id=account_id).first()
        old_balance = acc.balance
        acc.precredit = old_balance
        new_balnce = old_balance - amount
        acc.balance = new_balnce
        db.session.add(acc)
        print(new_balnce)
        return True
    except Exception as e:
        db.session.rollback()
        print(f"error '{e}'")
        return False


def commission_withdrawal(account_id, amount):
    try:
        acc = db.session.query(Credit).filter_by(id=account_id).first()
        old_balance = acc.balance
        new_balnce = old_balance - amount
        acc.balance = new_balnce
        db.session.add(acc)
        print(new_balnce)
        return True
    except Exception as e:
        db.session.rollback()
        print(f"error '{e}'")
        return False


def deposit(account_id, amount):
    try:
        acc = db.session.query(Credit).filter_by(id=account_id).first()
        old_balance = acc.balance
        acc.precredit = old_balance
        new_balnce = old_balance + amount
        acc.balance = new_balnce
        db.session.add(acc)
        print(new_balnce)
        return True
    except Exception as e:
        db.session.rollback()
        print(f"error '{e}'")
        return False


def commission_deposit(account_id, amount):
    try:
        acc = db.session.query(Credit).filter_by(id=account_id).first()
        old_balance = acc.balance
        new_balnce = old_balance + amount
        acc.balance = new_balnce
        db.session.add(acc)
        print(new_balnce)
        return True
    except Exception as e:
        db.session.rollback()
        print(f"error '{e}'")
        return False


def is_covered(user_id, req_amount):
    user_credit = db.session.query(Credit).filter_by(id=user_id).first()
    current_amount = user_credit.balance
    print(current_amount >= req_amount)
    return current_amount >= req_amount


def find_store(store_id):
    store = db.session.query(StoreInfo).filter_by(id=store_id).first()
    if store != None:
        return True
    return False


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'role': self.role,
            'phone': self.phone,
        }


def is_provider(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if user.role == 'provider':
        return True
    return False


def get_user_role(username):
    user = db.session.query(User).filter_by(
        username=username).first()
    return user.role


def get_user_id(username):
    user = db.session.query(User).filter_by(
        username=username).first()
    if user != None:
        return user.id
    return -1


def get_user_name(user_id):
    user = db.session.query(User).filter_by(
        id=user_id).first()
    return user.username


def find_user(username):
    user = db.session.query(User).filter_by(
        username=username).first()
    if user != None:
        return True
    return False


def find_user_phone(phone_number):
    user = db.session.query(User).filter_by(
        phone=phone_number).first()
    if user != None:
        return True
    return False


class Operation(db.Model):
    __tablename__ = 'operation'
    id = db.Column(db.Integer, primary_key=True)
    source_username = db.Column(db.String(10), nullable=False)
    destination_username = db.Column(db.String(10), nullable=False)
    provider_username = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(30), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    commission = db.Column(db.Integer, nullable=False)

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'source_username': self.source_username,
            'destination_username': self.destination_username,
            'provider_username': self.provider_username,
            'amount': self.amount,
            'time': self.time,
            'total': self.total,
            'commission': self.commission,

        }


def new_operation(source_username, destination_username, provider_username, amount, time, total, commission):
    current_time_str = time.strftime("%Y-%m-%d %H:%M")
    new_operation = Operation(source_username=source_username, destination_username=destination_username,
                              provider_username=provider_username, amount=amount, time=current_time_str, total=total,  commission=commission)
    try:
        db.session.add(new_operation)
        return True
    except Exception as e:
        db.session.rollback()
        return False


def get_operation_id(time):
    time_str = time.strftime("%Y-%m-%d %H:%M")
    operation = db.session.query(Operation).filter_by(time=time_str).first()
    return operation.id

    # We added this serialize function to be able to send JSON objects in a serializable format
