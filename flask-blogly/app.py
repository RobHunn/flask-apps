"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "victoriasecret"
debug = DebugToolbarExtension(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:$Treypostgresql74!@localhost:5432/blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
# db.create_all()


@app.route("/")
def home():
    users = User.query.all()
    return render_template("home.html", users=users)


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/adduser", methods=["POST"])
def user_add():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
    img_url = img_url if img_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/show_user/<int:id>")
def show_user(id):
    """Show info on a single user."""

    user = User.query.get_or_404(id)
    return render_template("user.html", user=user)


@app.route("/edit/<int:id>")
def edit(id):
    """Show info on a single user."""

    user = User.query.get_or_404(id)
    return render_template("user.html", user=user)


@app.route("/delete/<int:id>")
def delete(id):
    """Show info on a single user."""

    user = User.query.get_or_404(id)
    return render_template("user.html", user=user)
