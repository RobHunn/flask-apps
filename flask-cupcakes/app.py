"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
from models import db, connect_db, Cupcake

# from forms import AddPetForm
from shhh import hippo, victoriasecret

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = f"{victoriasecret}"
debug = DebugToolbarExtension(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{hippo}@localhost:5432/cupcake"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/cupcakes")
def all_cupcakes():
    """ Get data about all cupcakes """
    all_cakes = Cupcake.query.all()
    cakes = [cake.serialize() for cake in all_cakes]
    return jsonify(data=cakes)


@app.route("/api/cupcakes/<int:cupcake_id>")
def one_cupcake(cupcake_id):
    """  Get data about a single cupcake """
    one_cake = Cupcake.query.get_or_404(cupcake_id)
    cake = one_cake.serialize()
    return jsonify(data=cake)


@app.route("/api/cupcakes", methods=["POST"])
def post_cupcake():
    """ Create a cupcake with flavor, size, rating and image data """
    new_cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=request.json["image"]
        if request.json["image"]
        else "https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg",
    )
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(data=new_cupcake.serialize()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    cake = Cupcake.query.get_or_404(cupcake_id)

    cupcake_update = Cupcake.query.filter_by(id=cupcake_id).update(
        {
            Cupcake.flavor: request.json.get("flavor", cake.flavor),
            Cupcake.size: request.json.get("size", cake.size),
            Cupcake.rating: request.json.get("rating", cake.rating),
            Cupcake.image: request.json.get("image", cake.image),
        }
    )
    if cupcake_update:
        db.session.commit()
        return (jsonify(data=cake.serialize()), 201)
    else:
        return (jsonify({"message": "error item not found 404"}), 404)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cake)
    db.session.commit()
    return jsonify(message=f"Cupcake id: #{cake.id} is gone...")
