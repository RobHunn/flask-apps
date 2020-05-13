"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User Table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(
        db.String(200), nullable=False, default="../static/images/placeholder.jpg"
    )

    def __repr__(self):
        """Show info about user"""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    @classmethod
    def full_name(cls, id):
        """ Get user full name matching id passed """
        user = cls.query.filter(User.id == id).one_or_none()
        if user:
            first_name = user.first_name
            last_name = user.last_name
            return f"{first_name} {last_name}"
        else:
            return None

    @classmethod
    def delete_user(cls, id):
        """delte user by id"""
        user = cls.query.get(id)
        if user:
            delete = cls.query.filter(User.id == id).delete()
            db.session.commit()
            return delete
        else:
            delete = None
            return delete
