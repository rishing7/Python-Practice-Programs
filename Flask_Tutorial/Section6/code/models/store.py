from Flask_Tutorial.Section6.code.db import db
import sqlite3


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, price):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        """ Interaction with database."""
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name = ?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        #
        # connection.close()
        # if row:
        #     return cls(*row)

        """ After using sqlalchemy we can use above code as below."""

        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name = ? first helps to retrieve first row

    def save_to_db(self):       # this can for insertion and update
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        #
        # connection.commit()
        # connection.close()
        """ After using sqlalchemy we can use above code as below."""
        db.session.add(self)    # Instance of the ItemModel is to be inserted
        db.session.commit()

    """ Above method helps to update and insert"""
    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE items SET price = ? WHERE name = ?)"
    #     cursor.execute(query, (self.price, self.name))
    #
    #     connection.commit()
    #     connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()