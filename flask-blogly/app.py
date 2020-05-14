"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for, flash
from models import db, connect_db, User, Post

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "victoriasecret"
debug = DebugToolbarExtension(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:xxxxx@localhost:5432/blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()


@app.errorhandler(404)
def page_not_found(e):

    return render_template("404.html"), 404


@app.route("/")
def home():
    users = User.query.order_by(User.last_name, User.first_name).all()
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

    return redirect(url_for("show_user", id=user.id))


@app.route("/show_user/<int:id>")
def show_user(id):
    """Show info on a single user."""

    user = User.query.get_or_404(id)
    posts = Post.query.filter(Post.user_id == id).order_by(Post.created_at.desc()).all()
    return render_template("user.html", user=user, posts=posts)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    """Show edit form on GET, or edit user then Redirect on POST ."""

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image_url"]
        image_url = image_url if image_url else "../static/images/placeholder.jpg"

        user = User.query.filter(User.id == id).update(
            {
                User.first_name: first_name,
                User.last_name: last_name,
                User.image_url: image_url,
            }
        )
        db.session.commit()

        if user:
            return redirect(url_for("show_user", id=id))
        else:
            return "error"
    else:
        user = User.query.get_or_404(id)
        return render_template("edit.html", user=user)


@app.route("/delete/<int:id>")
def delete(id):
    """Delete single user."""

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))


##################################################################################
#
# -- Posts
#
##################################################################################


@app.route("/post_details/<int:id>")
def post_details(id):

    post = Post.query.get_or_404(id)
    return render_template("posts_details.html", post=post)


@app.route("/add_post/<user_id>")
def add_post(user_id):
    user = User.query.filter(User.id == user_id).all()
    user_name = User.full_name(user_id)
    return render_template("add_post.html", user_id=user_id, user_name=user_name)


@app.route("/new_post", methods=["POST"])
def new_post():
    id = request.form["user_id"]
    new_post = Post(
        title=request.form["title"], content=request.form["content"], user_id=id
    )

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(url_for("show_user", id=id))


@app.route("/edit_post/<int:id>", methods=["GET", "POST"])
def edit_post(id):

    if request.method == "POST":

        post = Post.query.filter(Post.id == id).update(
            {
                Post.title: request.form["title"],
                Post.content: request.form["content"],
                Post.user_id: request.form["user_id"],
            }
        )
        db.session.commit()
        # post.title = request.form["title"]
        # post.content = request.form["content"]

        # db.session.add(post)
        # db.session.commit()

        return redirect(url_for("post_details", id=id))

    else:
        post = Post.query.get_or_404(id)
        return render_template("posts_edit.html", post=post, user_id=post.user_id)


@app.route("/delete_post/<int:id>")
def delete_post(id):
    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(url_for("show_user", id=post.user_id))
