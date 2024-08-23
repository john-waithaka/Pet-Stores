"""_summary_
Explanation:

PetStore Model:
This model represents a pet store. It has an ID and a name.
The pets relationship links it to the Pet model, showing that a pet store can have many pets.


Pet Model:
This model represents a pet. It has an ID, name, type (e.g., dog, cat), and a store_id which links it to a PetStore.
The is_active field allows for soft deletion by marking a pet as inactive instead of removing it from the database.

"""


from . import db

class PetStore(db.Model):
    __tablename__ = 'pet_store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pet', backref='store', lazy=True)

    def __repr__(self):
        return f"<PetStore {self.name}>"


class Pet(db.Model):
    __tablename__ = 'pet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    store_id = db.Column(db.Integer, db.ForeignKey('pet_store.id'), nullable=False)

    def __repr__(self):
        return f"<Pet {self.name}, Type: {self.type}>"
