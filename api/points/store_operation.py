from api import db


class StoreOperation():

    def get_all_stores(self):
        try:
            stores = db.session.query(StoreInfo).all()
        except Exception as e:
            print('DB ERROR : ', e)
            return

        return stores

    def find_store(self, id):
        try:
            store = db.session.query(StoreInfo).filter_by(id=id).first()
        except Exception as e:
            print('DB ERROR : ', e)
        if store == None:
            return False
        return True

    def get_store(self, id):
        try:
            store = db.session.query(StoreInfo).filter_by(id=id).first()
        except Exception as e:
            print('DB ERROR : ', e)
            return
        return store

    def add_sotre(self, id, name, phone, balance):
        try:
            store = StoreInfo(id=id, name=name, phone=phone, balance=balance)
            db.session.add(store)
            db.session.commit()
        except Exception as e:
            print('DB ERROR : ', e)
            db.session.rollback()
            return
        return

    def delete_store(self, id):
        try:
            store = db.session.query(StoreInfo).filter_by(id=id).first()
            db.session.delete(store)
            db.session.commit()
        except Exception as e:
            print('DB ERROR : ', e)
            db.session.rollback()
            return
        return

    def update_store(self, id, name, phone, balance):
        try:
            store = db.session.query(StoreInfo).filter_by(id=id).first()
            store.name = name
            store.phone = phone
            store.balance = balance
            db.session.add(store)
            db.session.commit()
        except Exception as e:
            print('DB ERROR : ', e)
            db.session.rollback()
            return
        return

    def update_store_balance(self, id, balance):
        try:
            store = db.session.query(StoreInfo).filter_by(id=id).first()
            store.balance = balance
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError as e:
            print('DB ERROR : ', e)
            db.session.rollback()
            return
        return
