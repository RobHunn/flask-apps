"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

# from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """ Cupcake Table """

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(
        db.Text, nullable=False, default="https://tinyurl.com/demo-cupcake"
    )
    # species_tag = db.relationship("PetSpeciesTag", backref="species")

    def __repr__(self):
        """Show info about cupcakes"""
        u = self
        return f"<Cupcake id={u.id} flavor={u.flavor} size={u.size} rating={u.rating} image={u.image}>"

    def serialize(self):
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image,
        }
