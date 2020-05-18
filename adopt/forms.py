from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SelectField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf


class AddPetForm(FlaskForm):
    """Form for adding a pet."""

    name = StringField(
        "pet name", validators=[InputRequired(message="Pet name requiered")]
    )
    species = SelectField(
        "species",
        coerce=int,
        validators=[
            InputRequired(message="Pet species required"),
            AnyOf(
                values=[1, 2, 3],
                message="must be a valide species",
                values_formatter=None,
            ),
        ],
    )
    image_url = StringField(
        "image",
        validators=[
            Optional(),
            URL(require_tld=False, message="must be a real url,local host allowed"),
        ],
    )
    age = FloatField(
        "pet age",
        validators=[
            NumberRange(min=1, max=30, message="Pet age must be between 1-30"),
            InputRequired(message="Age requiered"),
        ],
    )
    notes = StringField("notes about pet")
    available = BooleanField(" available true or flase")
