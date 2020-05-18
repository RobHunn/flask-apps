"""Seed file to make sample data for adopt db."""

from models import Pet, Specie, PetSpeciesTag, db
from app import app

# Create all tables
db.session.rollback()
db.drop_all()
db.create_all()

#######  add species  #######

pet = Specie(species="Cat")
pet2 = Specie(species="Porcupine")
pet3 = Specie(species="Dog")

pets = [pet, pet2, pet3]

db.session.add_all(pets)
db.session.commit()

#######  add Pets  #######
whiskers = Pet(
    name="Whiskers",
    specie_id=1,
    image_url="https://static01.nyt.com/images/2019/12/20/arts/00cats-1/00cats-1-videoSixteenByNineJumbo1600-v3.jpg",
    age=2,
    notes="fun and playful cat...",
    available=True,
)
supercat = Pet(
    name="Supercat",
    specie_id=1,
    image_url="https://s7d2.scene7.com/is/image/TWCNews/0718_n13_universal_cats_taylor_swift",
    age=6,
    notes="Super awesome cat...",
    available=True,
)

jake = Pet(
    name="Jake",
    specie_id=2,
    image_url=None,
    age=3,
    notes="Super awesome porcupine...",
    available=False,
)
pettyPet = Pet(
    name="PettyPet",
    specie_id=3,
    image_url=None,
    age=8,
    notes="Super awesome dog...",
    available=False,
)

pets = [whiskers, supercat, jake, pettyPet]

db.session.add_all(pets)
db.session.commit()


#######  add to the join table PetSpeciesTag #######
x = PetSpeciesTag(pet_id=1, specie_id=1)
db.session.add(x)
db.session.commit()

xx = PetSpeciesTag(pet_id=2, specie_id=1)
db.session.add(xx)
db.session.commit()

xxx = PetSpeciesTag(pet_id=3, specie_id=2)
db.session.add(xxx)
db.session.commit()

xxxx = PetSpeciesTag(pet_id=4, specie_id=3)
db.session.add(xxxx)
db.session.commit()
