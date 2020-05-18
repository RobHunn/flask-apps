"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Specie(db.Model):
    """ Table name species / class name Specie / relationship """

    __tablename__ = "species"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    species = db.Column(db.String(100), nullable=False)
    species_tag = db.relationship("PetSpeciesTag", backref="species")

    def __repr__(self):
        """Show info about species"""
        u = self
        return f"<Specie id={u.id} species={u.species}>"


class Pet(db.Model):
    """ pets table / Pet model"""

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.Text, default="../static/placeholder.jpg")
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)
    specie_id = db.Column(db.Integer, db.ForeignKey("species.id"))

    specie = db.relationship("Specie", secondary="pet_species_tag", backref="pet")

    def __repr__(self):
        """Show info about user"""
        u = self
        return f"<Pet id={u.id} name={u.name} specie_id={u.specie_id} image_url={u.image_url} age={u.age} notes={u.notes} available={u.available}>"


class PetSpeciesTag(db.Model):
    """ Pet & species relationship table """

    __tablename__ = "pet_species_tag"

    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), primary_key=True)
    specie_id = db.Column(db.Integer, db.ForeignKey("species.id"), primary_key=True)

    def __repr__(self):
        """Show relationship with pet and species"""
        u = self
        return f"<PostTag pet_id={u.pet_id} specie_id={u.specie_id}>"
