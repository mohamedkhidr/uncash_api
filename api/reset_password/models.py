from random import randint
import datetime
from api import db


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
