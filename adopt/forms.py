from flask_wtf import FlaskForm
from wtforms import StringField, FloatField


class AddPetForm(FlaskForm):
    name = StringField("pet name")
    species = StringField("species")
    image_url = StringField("image")
    age = FloatField("pet age")
    notes = StringField("notes about pet")
    available = bool(" available true or flase")

