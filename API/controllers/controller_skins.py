from flask import jsonify, request
from models.models import *
from bson.objectid import ObjectId

def get_skins_available():
    try:
        # Obtener todas las filas de la colección skins
        available_skins = list(skins.find({}, {'_id': 0}))

        return jsonify({"skins": available_skins}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_skins_to_db(skins_data):

    # Insert skins into the collection
    skins.insert_many(skins_data)

    return "Skins added successfully!"

def add_skins():
    try:
        # Check if the request contains a JSON file
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        skins_data = json.load(file)

        result = add_skins_to_db(skins_data)

        return jsonify({"message": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_user_skins_info():
    try:
        json_data = request.get_json()
        user_id = json_data.get("user_id")

        if not user_id:
            return jsonify({"error": "User ID not provided"}), 400

        user_id_obj = ObjectId(user_id)
        user = users.find_one({"_id": user_id_obj})

        if user:
            user_owned_skins = user.get("owned_skins", [])
            user_skin_info = []

            for owned_skin in user_owned_skins:
                skin_id = owned_skin.get("skin")
                skin = skins.find_one({"_id": skin_id})
                if skin:
                    user_skin_info.append({
                        "id": str(skin_id),  # Use the string representation
                        "name": skin.get("name"),
                        "color": owned_skin.get("color"),
                        "rarity": skin.get("rarity")
                    })

            return jsonify({"skins": user_skin_info}), 200        

        else:
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def change_skin_color():
    try:
        json_data = request.get_json()
        user_id = json_data.get("user_id")
        
        if not user_id:
            return jsonify({"error": "User ID not provided"}), 400
        
        skin_id = json_data.get("skin")
        skin_id_obj = ObjectId(skin_id)

        if not skin_id:
            return jsonify({"error": "Skin id not provided"}), 400
        
        new_color = json_data.get("color")

        if not new_color:
            return jsonify({"error": "New color not provided"}), 400

        user_id_obj = ObjectId(user_id)
        user = users.find_one({"_id": user_id_obj})

        if user:
            try:
                users.update_one(
                    {'_id': user_id_obj, 'owned_skins.skin': skin_id_obj},
                    {'$set': {'owned_skins.$.color': new_color}}
                )
            except Exception as e:
                print(f'Error updating skin color: {e}')

            return jsonify({"message": f"Color for {skin_id} successfully changed to {new_color}."}), 200        

        else:
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

