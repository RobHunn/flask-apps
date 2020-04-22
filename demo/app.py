from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "victoriasecret"

debug = DebugToolbarExtension(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rob-flask-demo-app.db"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

db = SQLAlchemy(app)


class DemoTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default=None, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return str(self.id)


# To create the initial database, just import the db object from an interactive-
# Python shell and run the SQLAlchemy.create_all() method to create the tables and database:

# from yourapplication import db
# db.create_all()


@app.route("/")
def home():
    """Show home page + form."""
    return render_template("home.html")


@app.route("/posts", methods=["GET", "POST"])
def posts():
    """Show list-of-posts or make a post."""
    if request.method == "POST":
        post_title = request.form["title"]
        post_text = request.form["body"]
        post_author = request.form["author"]
        new_post = DemoTable(title=post_title, text=post_text, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")

    print("I am a get request...")
    posts = DemoTable.query.order_by(DemoTable.date_posted).all()
    return render_template("posts.html", posts=posts)
