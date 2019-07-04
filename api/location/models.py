from api import db


class Points(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.String(8), primary_key=True)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
        }


     def __repr__(self):
        return f"User('{self.id}', '{self.latitude}', '{self.longitude}')"


