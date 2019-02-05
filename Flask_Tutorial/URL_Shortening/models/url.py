from Programing.URL_Shortening.db import db


class URLModel(db.Model):
    """ SQLALCHEMY FORMAT FOR DATABASE CREATION."""
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    originalURL = db.Column(db.String(1000))
    shortURL = db.Column(db.String(100))

    def __init__(self, originalURL, shortURL):
        self.originalURL = originalURL
        self.shortURL = shortURL

    def json(self):
        """ Returns json format of data."""
        return {'originalURL': self.originalURL, 'shortURL': self.shortURL}

    @classmethod
    def find_by_name(cls, originalURL):
        """ Interaction with database."""
        return cls.query.filter_by(originalURL=originalURL).first()

    @classmethod
    def find_by_shortURL(cls, shortURL):
        """ Interaction with database."""
        return cls.query.filter_by(shortURL=shortURL).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()