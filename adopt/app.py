""" Adopt app """

from flask import Flask, request, redirect, render_template, url_for, flash
from models import db, connect_db, Pet
from forms import AddPetForm

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "victoriasecret"
debug = DebugToolbarExtension(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:xxxxx@localhost:5432/adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


@app.errorhandler(404)
def page_not_found(e):

    return render_template("404.html"), 404


@app.route("/")
def home():
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)


@app.route("/petform")
def add_pet():
    form = AddPetForm()
    return render_template("add_pet_form.html", form=form)
