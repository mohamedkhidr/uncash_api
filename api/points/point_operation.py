from api import db
from api.models import StoreInfo, Points, Credit


class PointOperation():

    def get_all_points(self):
        try:
            points = db.session.query(Points, StoreInfo, Credit).filter(
                Points.id == StoreInfo.id).all()
            return points
        except Exception as e:
            print('DB ERROR : ', e)

    def find_point(self, id):
        try:
            point = db.session.query(Points).filter_by(id=id).first()
        except Exception as e:
            print('DB ERROR : ', e)
            return False
        if point == None:
            return False
        return True

    def get_point(self, id):
        try:
            point = db.session.query(Points).filter_by(id=id).first()
        except Exception as e:
            print('DB ERROR : ', e)
            return
        return point

    def add_point(self, id, latitude, longitude):
        try:
            point = Points(id=id, latitude=latitude, longitude=longitude)
            db.session.add(point)
            db.session.commit()
        except Exception as e:
            print('DB ERROR : ', e)
            db.session.rollback()
            return
        return

    def delete_point(self, id):
        try:
            point = db.session.query(Points).filter_by(id=id).first()
            db.session.delete(point)
            db.session.commit()
        except Exception as e:
            print('DB ERROR : ', e)
            db.session.rollback()
            return
        return

    def update_point(self, id, latitude, longitude):
        try:
            point = db.session.query(Points).filter_by(id=id).first()
            point.id = id
            point.latitude = latitude
            point.longitude = longitude
            db.session.add(point)
            db.session.commit()
        except Exception as e:
            print('DB ERROR : ', e)
            db.session.rollback()
            return
        return
