"""Seed file to make sample data for blogly db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.session.rollback()
db.drop_all()
db.create_all()

####### add Users  #######
whiskey = User(
    first_name="Whiskey",
    last_name="drinking",
    image_url="https://www.thewhiskyexchange.com/media/rtwe/uploads/banners/1389_Large.jpg?v=439547488542",
)
bowser = User(
    first_name="Bowser",
    last_name="waters",
    image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTDU6uA1HXoA1XXpAwt0zA8tEpM29oDiRGGjC2upkXfCmkW1ruo&usqp=CAU",
)
spike = User(
    first_name="Spike",
    last_name="Boss",
    image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcR36MsOO7H1kKWWAlLTzwfeqhGF4hxwoNFsjOaPJPf2U1AqoVQG&usqp=CAU",
)

db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

db.session.commit()

####### add Tags  #######
tag = Tag(name="Technologies")
tag2 = Tag(name="Educational")
tag3 = Tag(name="Politics")
tag4 = Tag(name="Bootcamps")

tags = [tag, tag2, tag3, tag4]

db.session.add_all(tags)
db.session.commit()


####### add comments  #######
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

####### add PostTag #######

post_tag = PostTag(post_id=1, tag_id=1)
post_tag2 = PostTag(post_id=1, tag_id=2)
post_tag3 = PostTag(post_id=2, tag_id=1)
post_tag4 = PostTag(post_id=2, tag_id=4)
post_tag5 = PostTag(post_id=3, tag_id=1)
post_tag6 = PostTag(post_id=3, tag_id=2)
post_tag7 = PostTag(post_id=3, tag_id=3)
post_tag8 = PostTag(post_id=3, tag_id=4)

post_tags = [
    post_tag,
    post_tag2,
    post_tag3,
    post_tag4,
    post_tag5,
    post_tag6,
    post_tag7,
    post_tag8,
]

db.session.add_all(post_tags)
db.session.commit()
