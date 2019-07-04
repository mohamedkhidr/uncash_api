from api import db


class Credit(db.Model):
    __tablename__ = 'credit'
    id = db.Column(db.String(8), primary_key=True)
    balance = db.Column(db.Integer, nullable=False)
    precredit = db.Column(db.Integer, nullable=False)

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'balance': self.balance,
        }


     def __repr__(self):
        return f"User('{self.id}', '{self.balance}')"





class Operation(db.Model):
    __tablename__ = 'operation'
    id = db.Column(db.String(10), primary_key=True)
    source_id = db.Column(db.String(8), nullable=False)
    destination_id = db.Column(db.String(8), nullable=False)
    amount = db.Column(db.Integer , nullable=False)
    status = db.Column(db.String(10), nullable=False)
    source_amount = db.Column(db.Integer, nullable=False)
    destination_amount = db.Column(db.Integer, nullable=False)


    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'source_id': self.source_id,
            'destination_id': self.destination_id,
            'amount': self.amount,
            'status': self.status,
            'source_amount': self.source_amount,
            'destination_amount': self.destination_amount,
        }



    def __repr__(self):
        return f"User('{self.id}', '{self.source_id}', '{self.destination_id}', '{self.source_amount}','{self.destination_amount}','{self.amount}',,'{self.status}')"


