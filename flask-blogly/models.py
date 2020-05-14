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
        return f"<User {u.id} {u.title} {content} {u.user_id}>"


# post=Post(title='i am title',content='i am a post content, hope this is not too long orther wise i might not see it',user_id=1)

# In [10]: db.session.add(post)

# In [11]: db.session.commit()


# In [6]: user = User(first_name='Robert',last_name='Bobby',image_url=None)

# In [7]: db.session.add(user)

# In [8]: db.session.commit()
