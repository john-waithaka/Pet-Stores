from flask import Blueprint, request, jsonify
from . import db
from .models import PetStore, Pet

main = Blueprint('main', __name__)

# Simple in-memory cache
pet_cache = {}

# 1. Create a new pet (POST)
@main.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json()
    new_pet = Pet(
        name=data.get('name'),
        type=data.get('type'),
        store_id=data.get('store_id')
    )
    db.session.add(new_pet)
    db.session.commit()
    
    # Invalidate cache after adding a new pet
    pet_cache.clear()
    
    return jsonify({"message": "Pet created successfully!"}), 201

# 2. Read a single pet (GET)
@main.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    # Check cache first
    if id in pet_cache:
        return jsonify(pet_cache[id])
    
    # Query the database if not in cache
    pet = Pet.query.get_or_404(id)
    if not pet.is_active:
        return jsonify({"message": "Pet is not available."}), 404

    pet_data = {
        "id": pet.id,
        "name": pet.name,
        "type": pet.type,
        "store_id": pet.store_id,
        "is_active": pet.is_active
    }

    # Store in cache
    pet_cache[id] = pet_data

    return jsonify(pet_data)

# 3. Read all pets (GET)
@main.route('/pets', methods=['GET'])
def get_pets():
    # Cache key for all active pets
    all_pets_key = 'all_active_pets'
    
    # Check cache first
    if all_pets_key in pet_cache:
        return jsonify(pet_cache[all_pets_key])

    # Query the database if not in cache
    pets = Pet.query.filter_by(is_active=True).all()
    pets_list = [{"id": pet.id, "name": pet.name, "type": pet.type, "store_id": pet.store_id} for pet in pets]
    
    # Store in cache
    pet_cache[all_pets_key] = pets_list

    return jsonify(pets_list)

# 4. Update a pet (PUT)
@main.route('/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    pet = Pet.query.get_or_404(id)
    data = request.get_json()

    pet.name = data.get('name', pet.name)
    pet.type = data.get('type', pet.type)
    db.session.commit()
    
    # Update cache
    pet_cache.pop(id, None)  # Invalidate specific pet in cache

    return jsonify({"message": "Pet updated successfully!"})

# 5. Soft delete a pet (DELETE)
@main.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    pet = Pet.query.get_or_404(id)
    pet.is_active = False
    db.session.commit()
    
    # Invalidate cache after deletion
    pet_cache.pop(id, None)  # Remove specific pet from cache
    pet_cache.pop('all_active_pets', None)  # Invalidate all active pets cache

    return jsonify({"message": "Pet soft-deleted successfully!"})

# 6. Restore a soft-deleted pet (PUT)
@main.route('/pets/restore/<int:id>', methods=['PUT'])
def restore_pet(id):
    pet = Pet.query.get_or_404(id)
    pet.is_active = True
    db.session.commit()
    
    # Invalidate cache after restoring
    pet_cache.pop(id, None)  # Remove specific pet from cache
    pet_cache.pop('all_active_pets', None)  # Invalidate all active pets cache

    return jsonify({"message": "Pet restored successfully!"})


