"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User
from datetime import datetime


class Post(db.Model):
    """ Post Table"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref=("posts", cascade="all, delete-orphan"))

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
