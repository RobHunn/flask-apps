"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """ pets table / Pet model"""

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.Text, default="../static/placeholder.jpg")
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)
    # posts = db.relationship("Post", backref="user",
    #                         cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user"""
        u = self
        return f"<Pet id={u.id} name={u.name} species={u.species} image_url={u.image_url} age={u.age} notes={u.notes} available={u.available}>"
