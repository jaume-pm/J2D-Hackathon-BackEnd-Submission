from flask import jsonify, request
from models.models import *
from bson.objectid import ObjectId
from utilities.getters import *

def get_skins_available():
    try:
        # Obtener todas las filas de la colección skins
        available_skins = list(skins.find({}, {'_id': 0}))

        return jsonify({"skins": available_skins}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_skins():
    try:
        # Check if the request contains a JSON file
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        skins_data = json.load(file)

        skins.insert_many(skins_data)

        return jsonify({"result": "OK"}), 200

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

        user_id = get_user_id(json_data)
        skin_id = get_skin_id(json_data)
        color = get_skin_color(json_data)

        user = users.find_one({"_id": user_id})

        if user:
            try:
                result = users.update_one(
                    {'_id': user_id, 'owned_skins.skin': skin_id},
                    {'$set': {'owned_skins.$.color': color}}
                )
                if result.matched_count == 0:
                    return jsonify({"error": "No matching skin found"}), 404                
                else:
                    return jsonify({"result": "OK"}), 200 
              
            except Exception as e:
                return jsonify({"error": f"Error updating skin color: {str(e)}"}), 500
        else:
            return jsonify({"error": f"No user found with ID: {user_id}"}), 404

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


