"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User Table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(
        db.String(200), nullable=False, default="../static/images/placeholder.jpg"
    )
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user"""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    @classmethod
    def full_name(cls, id):
        """ Get user full name matching id passed """
        user = cls.query.filter(User.id == id).one_or_none()
        if user:
            first_name = user.first_name
            last_name = user.last_name
            return f"{first_name} {last_name}"
        else:
            return None


class Post(db.Model):
    """ Post Table"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        """Show info about post"""
        u = self
        content = (u.content[:75] + "...") if len(u.content) > 35 else u.content
        return f"<Post {u.id} {u.title} {content} {u.user_id}>"


class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        """Show info about a tag"""
        return f"<Tag name={self.name}>"

    posts = db.relationship(
        "Post", secondary="posts_tags", cascade="all,delete", backref="tags",
    )


class PostTag(db.Model):
    """ Post & tags relationship table """

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        """Show info about post"""
        u = self
        return f"<PostTag post_id={u.post_id} tag_id={u.tag_id}>"
