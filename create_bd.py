from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zyjepzflpuvetl:980d6c84bb514096f28acb2090c7eddd8d48da95ab00794907bfa7d75d2fc8b4@ec2-50-19-222-129.compute-1.amazonaws.com:5432/d5hjv1ppij20qf'
db = SQLAlchemy(app)


class OurCommissions(db.Model):
    __tablename__ = 'commissions'
    id = db.Column(db.Integer, primary_key=True)
    operation_id = db.Column(db.Integer, unique=True)
    amount = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)


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


class Codes(db.Model):
    EXPIRES = 15
    id = db.Column(db.Integer, primary_key=True)
    code_number = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)

    def check_validity(self, code_id):
        code = db.session.query(Codes).filter_by(id=code_id).first()
        current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        current_time = datetime.datetime.strptime(
            current_time_str, "%Y-%m-%d %H:%M")
        code_time = datetime.datetime.strptime(code.time, "%Y-%m-%d %H:%M")
        diff = current_time - code_time
        print(diff.seconds / 60)
        return (int(diff.seconds / 60) < self.EXPIRES)

    def send_code_number(self):

        from twilio.rest import Client
        self.phone_number = '+2' + self.phone_number
        # Your Account SID from twilio.com/console
        account_sid = "AC41fba35f701f4881c2d060eb4f2c703d"
        # Your Auth Token from twilio.com/console
        auth_token = "eec13458ffae8585468bfd6aab66b22c"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=self.phone_number, from_="+19382383325",
            body=f'your uncash verification code is {self.code_number}')


def find_code(code_number, phone_number):
    filter_codes()
    code = db.session.query(Codes).filter_by(
        code_number=code_number, phone_number=phone_number).first()

    return code


def generate_code(phone_number):
    filter_codes()
    code_number = randint(23657896, 99999999)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    phone_number = phone_number
    new_code = Codes(code_number=code_number,
                     time=time, phone_number=phone_number)

    db.session.add(new_code)
    db.session.commit()
    return new_code
# remove expired ones


def filter_codes():
    codes = db.session.query(Codes).all()
    for code in codes:
        if not code.check_validity(code.id):
            db.session.delete(code)
            db.session.commit()


class PhoneNumber(db.Model):
    EXPIRES = 15
    __tablename__ = 'phone_number'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)

    def check_validity(self, phone_id):
        number = db.session.query(
            PhoneNumber).filter_by(id=phone_id).first()
        current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        current_time = datetime.datetime.strptime(
            current_time_str, "%Y-%m-%d %H:%M")
        phone_time = datetime.datetime.strptime(number.time, "%Y-%m-%d %H:%M")
        diff = current_time - phone_time
        return (int(diff.seconds / 60) < self.EXPIRES)


def add_verified_number(phone_number):
    filter_phone_numbers()
    if find_number(phone_number) == None:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        db.session.add(PhoneNumber(phone_number=phone_number,
                                   time=time))
        db.session.commit()


def find_number(phone_number):
    filter_phone_numbers()
    number = db.session.query(PhoneNumber).filter_by(
        phone_number=phone_number).first()
    return number


def filter_phone_numbers():
    numbers = db.session.query(PhoneNumber).all()
    for number in numbers:
        if not number.check_validity(number.id):
            db.session.delete(number)
            db.session.commit()


class CodesReset(db.Model):
    EXPIRES = 15
    __tablename__ = 'codes_reset'
    id = db.Column(db.Integer, primary_key=True)
    code_number = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)

    def check_validity(self, code_id):
        code = db.session.query(CodesReset).filter_by(id=code_id).first()
        current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        current_time = datetime.datetime.strptime(
            current_time_str, "%Y-%m-%d %H:%M")
        code_time = datetime.datetime.strptime(code.time, "%Y-%m-%d %H:%M")
        diff = current_time - code_time
        print(diff.seconds / 60)
        return (int(diff.seconds / 60) < self.EXPIRES)

    def send_code_number(self):
        '''
        from twilio.rest import Client
        self.phone_number = '+2' + self.phone_number
        # Your Account SID from twilio.com/console
        account_sid = "ACbaa1bb5506f45925076cd1a382377bd1"
        # Your Auth Token from twilio.com/console
        auth_token = "2c71a7a60bd8f890bc620163a66089d9"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=self.phone_number, from_="+19803521976",
            body=f'your uncash verification code is {self.code_number}')
            '''


def find_code(code_number, phone_number):
    filter_codes()
    code = db.session.query(CodesReset).filter_by(
        code_number=code_number, phone_number=phone_number).first()

    return code


def generate_code(phone_number):
    filter_codes()
    code_number = randint(23657896, 99999999)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    phone_number = phone_number
    new_code = CodesReset(code_number=code_number,
                          time=time, phone_number=phone_number)

    db.session.add(new_code)
    db.session.commit()
    return new_code
# remove expired ones


def filter_codes():
    codes = db.session.query(CodesReset).all()
    for code in codes:
        if not code.check_validity(code.id):
            db.session.delete(code)
            db.session.commit()


class PhoneNumberReset(db.Model):
    EXPIRES = 15
    __tablename__ = 'phone_number_reset'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)

    def check_validity(self, phone_id):
        number = db.session.query(
            PhoneNumberReset).filter_by(id=phone_id).first()
        current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        current_time = datetime.datetime.strptime(
            current_time_str, "%Y-%m-%d %H:%M")
        phone_time = datetime.datetime.strptime(number.time, "%Y-%m-%d %H:%M")
        diff = current_time - phone_time
        return (int(diff.seconds / 60) < self.EXPIRES)


def add_verified_number(phone_number):
    filter_phone_numbers()
    if find_number(phone_number) == None:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        db.session.add(PhoneNumberReset(phone_number=phone_number,
                                        time=time))
        db.session.commit()


def find_number(phone_number):
    filter_phone_numbers()
    number = db.session.query(PhoneNumberReset).filter_by(
        phone_number=phone_number).first()
    return number


def filter_phone_numbers():
    numbers = db.session.query(PhoneNumberReset).all()
    for number in numbers:
        if not number.check_validity(number.id):
            db.session.delete(number)
            db.session.commit()


db.create_all()
