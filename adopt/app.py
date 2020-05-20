""" Adopt app """

from flask import Flask, request, redirect, render_template, url_for, flash
from models import db, connect_db, Pet, Specie, PetSpeciesTag
from forms import AddPetForm
from shhh import hippo

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "victoriasecret"
debug = DebugToolbarExtension(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{hippo}@localhost:5432/adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


@app.errorhandler(404)
def page_not_found(e):

    return render_template("404.html"), 404


@app.route("/")
def home():
    pets = (
        db.session.query(
            Pet.name,
            Pet.id,
            Pet.age,
            Pet.image_url,
            Pet.notes,
            Pet.available,
            Specie.species,
        )
        .join(Specie)
        .all()
    )
    return render_template("home.html", pets=pets)


@app.route("/petform", methods=["GET", "POST"])
def add_pet():
    form = AddPetForm()
    spec = db.session.query(Specie.id, Specie.species)
    form.species.choices = spec
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        species = form.species.data
        image_url = form.image_url.data
        image_url = image_url if image_url else None
        notes = form.notes.data
        available = form.available.data
        new_pet = Pet(
            name=name,
            age=age,
            specie_id=species,
            image_url=image_url,
            notes=notes,
            available=available,
        )
        db.session.add(new_pet)
        db.session.commit()
        flash(
            f"Pet created, name={name}, age={age}, specie_id={species}, image-url={image_url}, notes={notes} available={available}"
        )
        db.session.refresh(new_pet)
        db.session.add(PetSpeciesTag(pet_id=new_pet.id, specie_id=new_pet.specie_id))
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("add_pet_form.html", form=form)


@app.route("/edit_pet/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet)
    spec = db.session.query(Specie.id, Specie.species)
    form.species.choices = spec
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.age = form.age.data
        pet.species = form.species.data
        image_url = form.image_url.data
        pet.image_url = image_url if image_url else None
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for("pet_details", pet_id=pet.id))

    else:
        pet = (
            db.session.query(Pet.name, Pet.image_url, Pet.id)
            .filter(Pet.id == pet_id)
            .one()
        )
        return render_template("edit_pet_form.html", form=form, pet=pet)


@app.route("/pet_details/<int:pet_id>", methods=["GET"])
def pet_details(pet_id):
    pet = (
        db.session.query(
            Pet.name,
            Pet.id,
            Pet.age,
            Pet.image_url,
            Pet.notes,
            Pet.available,
            Specie.species,
        )
        .join(Specie)
        .filter(Pet.id == pet_id)
        .first()
    )

    return render_template("pet_details.html", pet=pet)
