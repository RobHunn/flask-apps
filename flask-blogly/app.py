"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for, flash
from models import db, connect_db, User, Post, Tag, PostTag

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "victoriasecret"
debug = DebugToolbarExtension(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:XXXXXX@localhost:5432/blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


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
    tags = (
        db.session.query(Tag.name, Tag.id)
        .join(PostTag)
        .filter(PostTag.post_id == post.id)
    )
    print("HIT TAGS ---->", tags)
    return render_template("posts_details.html", post=post, tags=tags)


@app.route("/add_post/<user_id>")
def add_post(user_id):
    user = User.query.filter(User.id == user_id).all()
    user_name = User.full_name(user_id)
    tags = Tag.query.all()
    return render_template(
        "add_post.html", user_id=user_id, user_name=user_name, tags=tags
    )


@app.route("/new_post", methods=["POST"])
def new_post():
    id = request.form["user_id"]
    new_post = Post(
        title=request.form["title"], content=request.form["content"], user_id=id
    )

    db.session.add(new_post)
    db.session.commit()

    db.session.refresh(new_post)
    print("HIT------>", new_post.id)
    values = request.form.getlist("checkbox")
    for tagID in values:
        insert_tags = PostTag(post_id=new_post.id, tag_id=tagID)
        db.session.add(insert_tags)
        db.session.commit()

    flash(f"Post '{new_post.title}' added.")
    return redirect(url_for("show_user", id=id))


@app.route("/edit_post/<int:id>", methods=["GET", "POST"])
def edit_post(id):

    if request.method == "POST":

        post = Post.query.get_or_404(id)
        post.title = request.form["title"]
        post.content = request.form["content"]
        tag_ids = [int(num) for num in request.form.getlist("checkbox")]
        post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        db.session.commit()

        return redirect(url_for("post_details", id=id))

    else:
        post = Post.query.get_or_404(id)
        tags = Tag.query.all()
        return render_template(
            "posts_edit.html", post=post, user_id=post.user_id, tags=tags
        )


@app.route("/delete_post/<int:id>")
def delete_post(id):
    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(url_for("show_user", id=post.user_id))


##################################################################################
#
# -- Tags -n- such
#
##################################################################################


@app.route("/match_all_tags/<int:tag_id>", methods=["GET"])
def match_all_tags(tag_id):
    posts = db.session.query(PostTag.post_id).join(Tag).filter(Tag.id == tag_id).all()
    posts = Post.query.filter(Post.id.in_(posts)).all()
    tag = Tag.query.get_or_404(tag_id)
    return render_template("post_list.html", posts=posts, tag=tag)
