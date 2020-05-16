"""Seed file to make sample data for adopt db."""

from models import Pet, db
from app import app

# Create all tables
db.session.rollback()
db.drop_all()
db.create_all()

####### add Users  #######
whiskers = Pet(
    name="Whiskers",
    species="Cat",
    image_url="https://static01.nyt.com/images/2019/12/20/arts/00cats-1/00cats-1-videoSixteenByNineJumbo1600-v3.jpg",
    age=2,
    notes="fun and playful cat...",
    available=True,
)
supercat = Pet(
    name="Supercat",
    species="Cat",
    image_url="https://s7d2.scene7.com/is/image/TWCNews/0718_n13_universal_cats_taylor_swift",
    age=6,
    notes="Super awesome cat...",
    available=True,
)

jake = Pet(
    name="Jake",
    species="Dog",
    image_url=None,
    age=3,
    notes="Super awesome dog...",
    available=False,
)

pets = [whiskers, supercat, jake]

db.session.add_all(pets)
db.session.commit()
