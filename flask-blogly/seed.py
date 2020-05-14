"""Seed file to make sample data for blogly db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
whiskey = User(first_name="Whiskey", last_name="drining", image_url=None)
bowser = User(first_name="Bowser", last_name="waters", image_url=None)
spike = User(first_name="Spike", last_name="porcupine", image_url=None)

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()


# add comments
user = User.query.filter(User.first_name == "Whiskey").one_or_none()
whiskey_comments = Post(
    title="I am whisky title", content="I am wishky content", user_id=user.id
)
db.session.add(whiskey_comments)
db.session.commit()

user2 = User.query.filter(User.first_name == "Bowser").one()
bowser_comments = Post(
    title="I am boswer title", content="I am boswer content", user_id=user2.id
)
db.session.add(bowser_comments)
db.session.commit()

user3 = User.query.filter(User.first_name == "Spike").one()
spike_comments = Post(
    title="I am a spike title", content="I am spikes content", user_id=user3.id
)
db.session.add(spike_comments)
db.session.commit()
